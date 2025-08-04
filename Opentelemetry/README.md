# OpenTelemetry

OpenTelemetry is an open-source observability framework for collecting, processing, and exporting telemetry data (traces, metrics, and logs). It provides a single set of APIs, libraries, agents, and collector services to capture distributed traces and metrics from your application.

## Traces

A trace is a representation of a single transaction or request as it flows through a distributed system. It is composed of one or more spans.

### Creating Custom Traces

To create a custom trace, you need to create a `TracerProvider`, get a `Tracer`, and then create a `Span`.

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

# Set up a TracerProvider
trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()

# Configure a ConsoleSpanExporter
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
tracer_provider.add_span_processor(span_processor)

# Get a Tracer
tracer = trace.get_tracer(__name__)

# Create a Span
with tracer.start_as_current_span("my-custom-span") as span:
    # Do some work here
    span.set_attribute("my-attribute", "my-value")
    print("Hello, world!")
```

### Exporting Traces to AWS X-Ray

To export traces to AWS X-Ray, you'll typically use the AWS Distro for OpenTelemetry (ADOT) Python SDK.

First, install the necessary packages:
```bash
pip install opentelemetry-sdk-extension-aws opentelemetry-propagator-aws-xray
```

Then, configure your `TracerProvider` to use the AWS X-Ray ID generator and propagator:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
from opentelemetry.sdk.extension.aws.trace.propagators import AwsXRayPropagator
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter # Replace with actual X-Ray exporter

# Set up a TracerProvider with AWS X-Ray ID generator
resource = Resource.create({"service.name": "my-aws-service"})
trace.set_tracer_provider(
    TracerProvider(resource=resource, id_generator=AwsXRayIdGenerator())
)
tracer_provider = trace.get_tracer_provider()

# Configure the AWS X-Ray propagator globally
from opentelemetry.propagate import set_global_textmap
set_global_textmap(AwsXRayPropagator())

# Configure an exporter (e.g., ConsoleSpanExporter for demonstration, replace with AWS X-Ray exporter)
# In a real scenario, you would use an OTLP exporter pointing to an ADOT Collector
# or a direct AWS X-Ray exporter if available.
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
tracer_provider.add_span_processor(span_processor)

# Get a Tracer
tracer = trace.get_tracer(__name__)

# Create a Span
with tracer.start_as_current_span("my-aws-xray-span") as span:
    span.set_attribute("aws.region", "us-east-1")
    print("Hello from AWS X-Ray trace!")

# Ensure to shut down the provider to export any buffered spans
tracer_provider.shutdown()
```

## Logs

Logs are timestamped text records, either structured or unstructured, with metadata.

### Creating a Custom Log Exporter

To create a custom log exporter, you need to create a class that inherits from `LogExporter` and implements the `export` method.

```python
from opentelemetry.sdk.logs import LogExporter, LogRecord
from opentelemetry.sdk.logs.export import BatchLogProcessor
from opentelemetry.sdk.logs import LoggerProvider, set_logger_provider
import logging

class MyCustomLogExporter(LogExporter):
    def export(self, batch: typing.Sequence[LogRecord]) -> None:
        for record in batch:
            print(f"My custom exporter: {record.body}")

# Set up a LoggerProvider
logger_provider = LoggerProvider()
set_logger_provider(logger_provider)

# Configure the custom exporter
exporter = MyCustomLogExporter()
logger_provider.add_log_processor(BatchLogProcessor(exporter))

# Get a Logger
logger = logging.getLogger(__name__)

# Log a message
logger.warning("This is a test log message.")
```

### Exporting Traces, Logs, and Metrics to Azure Monitor

To export telemetry to Azure Monitor, you can use the `azure-monitor-opentelemetry` distro.

First, install the necessary package:
```bash
pip install azure-monitor-opentelemetry --pre
```

Then, configure Azure Monitor collection. Ensure the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable is set.

```python
import os
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace, metrics
import logging

# Configure Azure Monitor collection
# Ensure APPLICATIONINSIGHTS_CONNECTION_STRING environment variable is set
configure_azure_monitor()

# Example for Tracing
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-azure-span"):
    print("Hello from Azure trace!")

# Example for Metrics
meter = metrics.get_meter(__name__)
counter = meter.create_counter("my_azure_counter", description="My custom counter for Azure")
counter.add(1)

# Example for Logging
logger = logging.getLogger(__name__)
logger.warning("This is a warning log for Azure.")

# In a real application, you would typically shut down providers when the application exits.
# For demonstration purposes, we don't explicitly shut down here as configure_azure_monitor handles it.
```

## Metrics

Metrics are a numerical representation of a value at a specific point in time.

### Creating Custom Metrics

To create a custom metric, you need to create a `MeterProvider`, get a `Meter`, and then create an instrument (e.g., a counter).

```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

# Set up a MeterProvider
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Get a Meter
meter = metrics.get_meter(__name__)

# Create a Counter
counter = meter.create_counter(
    "my-custom-counter",
    description="A counter for my custom metric",
    unit="1",
)

# Increment the counter
counter.add(1, {"my-attribute": "my-value"})
```

### Exporting Metrics to Prometheus

To export OpenTelemetry metrics to Prometheus, you can use the `opentelemetry-exporter-prometheus` library. This sets up an HTTP endpoint that Prometheus can scrape.

First, install the necessary packages:
```bash
pip install opentelemetry-exporter-prometheus prometheus_client
```

Then, configure your `MeterProvider` with the `PrometheusMetricsExporter` and start the Prometheus client HTTP server:

```python
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from prometheus_client import start_http_server

# Start Prometheus client HTTP server on port 8000
# This is where Prometheus will scrape metrics from.
start_http_server(port=8000, addr="localhost")

# Configure the MeterProvider
meter_provider = MeterProvider()
metrics.set_meter_provider(meter_provider)

# Create a PrometheusMetricsExporter instance
exporter = PrometheusMetricsExporter(prefix="my_application")

# Configure a PeriodicExportingMetricReader to push metrics to the exporter
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
meter_provider.add_metric_reader(reader)

# Get a Meter
meter = metrics.get_meter(__name__)

# Create a Counter metric
requests_counter = meter.create_counter(
    name="requests_total",
    description="Total number of requests",
    unit="1",
)

# Record a metric value
labels = {"environment": "development", "service": "my-app"}
requests_counter.add(1, attributes=labels)

print("Metrics are being exposed on http://localhost:8000/metrics")
print("Press Ctrl+C to exit...")
try:
    while True:
        time.sleep(1) # Keep the server running
except KeyboardInterrupt:
    print("Stopping Prometheus metrics exporter.")
finally:
    # Ensure to shut down the provider to export any buffered metrics
    metrics.get_meter_provider().shutdown()
```

**Explanation:**

*   **`start_http_server`**: This function from `prometheus_client` starts a basic HTTP server that exposes the metrics in a format Prometheus can scrape.
*   **`MeterProvider`**: Manages metrics in your application.
*   **`PrometheusMetricsExporter`**: Converts OpenTelemetry metrics into a Prometheus-compatible format.
*   **`PeriodicExportingMetricReader`**: Periodically collects metrics and pushes them to the exporter.
*   **`meter.create_counter`**: Creates a counter metric. Other types like Gauges and Histograms are also available.
*   **`requests_counter.add`**: Records a value for the counter with optional labels.

For more complex setups or production environments, it's a best practice to use the OpenTelemetry Collector. The Collector can receive telemetry data (including metrics) from your application via OTLP and then export it to various backends, including Prometheus. This provides more flexibility for processing, filtering, and routing your telemetry data.

### Exporting Traces, Logs, and Metrics to Google Cloud

To export telemetry to Google Cloud, you'll need to install the specific Google Cloud exporters and configure your application.

First, install the necessary packages:
```bash
pip install opentelemetry-exporter-gcp-trace \
            opentelemetry-exporter-gcp-monitoring \
            opentelemetry-exporter-gcp-logging \
            opentelemetry-sdk-extension-resource-detector-gcp
```

Then, configure your `TracerProvider`, `MeterProvider`, and `LoggerProvider` with the Google Cloud exporters:

```python
import logging
import time

from opentelemetry import trace, metrics
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.exporter.cloud_logging import CloudLoggingExporter
from opentelemetry_sdk_extension_resource_detector_gcp import GoogleCloudResourceDetector

# 1. Define a Resource
resource = GoogleCloudResourceDetector().detect()
resource = resource.merge(Resource.create({
    "service.name": "my-python-app",
    "service.instance.id": "instance-123",
    "service.version": "1.0.0",
}))

# --- Traces Configuration ---
def setup_tracing():
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    cloud_trace_exporter = CloudTraceSpanExporter()
    tracer_provider.add_span_processor(BatchSpanProcessor(cloud_trace_exporter))
    return trace.get_tracer(__name__)

# --- Metrics Configuration ---
def setup_metrics():
    cloud_monitoring_exporter = CloudMonitoringMetricsExporter()
    metric_reader = PeriodicExportingMetricReader(
        cloud_monitoring_exporter,
        export_interval_millis=5000
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    return metrics.get_meter(__name__)

# --- Logs Configuration ---
def setup_logging():
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    cloud_logging_exporter = CloudLoggingExporter(default_log_name="my-application-logs")
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(cloud_logging_exporter))
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    app_logger = logging.getLogger("my_app_logger")
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(handler)
    return app_logger

# --- Main Application Logic (Example Usage) ---
if __name__ == "__main__":
    tracer = setup_tracing()
    meter = setup_metrics()
    app_logger = setup_logging()

    request_counter = meter.create_counter(
        name="requests_total",
        description="Total number of requests",
        unit="1"
    )

    print("OpenTelemetry configured for Google Cloud. Generating telemetry...")

    with tracer.start_as_current_span("example-gcp-operation") as span:
        app_logger.info("Starting example operation for GCP.")
        request_counter.add(1, {"endpoint": "/gcp-example", "status": "success"})
        time.sleep(1)
        app_logger.warning("Completed example operation for GCP.")

    print("Telemetry generation complete. Waiting for exporters to flush...")
    time.sleep(10)

    trace.get_tracer_provider().shutdown()
    metrics.get_meter_provider().shutdown()
    set_logger_provider(None)
    print("Exporters shut down.")
```

### Collecting System Metrics (CPU, Memory, GC Stats)

To collect system and process metrics like CPU, memory usage, and garbage collection statistics, you can use the `opentelemetry-instrumentation-system-metrics` package. The calculation of aggregates like average, P99, and P90 is typically handled by the observability backend.

First, install the necessary package:
```bash
pip install opentelemetry-instrumentation-system-metrics
```

Then, instrument your application to collect these metrics:

```python
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

# Set up a MeterProvider with a ConsoleMetricExporter for demonstration
# In a real scenario, you would use an exporter for your chosen backend (e.g., Prometheus, Cloud Monitoring)
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Instrument system metrics
# This will automatically collect CPU, memory, and GC stats
SystemMetricsInstrumentor().instrument()

print("Collecting system metrics... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(5) # Metrics are exported periodically
except KeyboardInterrupt:
    print("Stopping system metrics collection.")
finally:
    # Ensure to shut down the provider to export any buffered metrics
    metrics.get_meter_provider().shutdown()
```

**Note on Aggregates (Average, P99, P90):**
While the OpenTelemetry Python SDK provides the raw data for these system metrics, the computation of statistical aggregates like average, P99 (99th percentile), and P90 (90th percentile) is typically handled by your chosen observability backend. These backends process the collected data, especially from Histogram instruments, to derive and visualize these percentile values and averages.

## Integrating OpenTelemetry into Existing Codebases: The TelemetryService

For robust and scalable OpenTelemetry integration in existing applications, especially in enterprise environments, it's best practice to centralize the setup and management of telemetry components. A `TelemetryService` class can encapsulate the initialization of tracing, logging, and metrics, ensuring consistent configuration and proper shutdown.

This approach leverages OTLP (OpenTelemetry Protocol) exporters, which are the recommended way to send telemetry data to an OpenTelemetry Collector. The Collector can then process, filter, and export the data to various backends (e.g., Prometheus, Jaeger, Loki, cloud-specific monitoring services) without requiring direct exporter dependencies in your application.

First, install the necessary OTLP exporter packages:
```bash
pip install opentelemetry-exporter-otlp
```

Here's an example of a `TelemetryService`:

```python
import logging
from opentelemetry import trace, metrics
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

class TelemetryService:
    def __init__(self, service_name: str, service_version: str = "1.0.0"):
        self.service_name = service_name
        self.service_version = service_version
        self.resource = Resource.create({
            "service.name": self.service_name,
            "service.version": self.service_version,
        })

        self.tracer_provider = None
        self.meter_provider = None
        self.logger_provider = None

    def initialize_tracing(self):
        self.tracer_provider = TracerProvider(resource=self.resource)
        trace.set_tracer_provider(self.tracer_provider)
        otlp_exporter = OTLPSpanExporter()
        self.tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        print(f"Tracing initialized for service: {self.service_name}")

    def initialize_metrics(self):
        otlp_exporter = OTLPMetricExporter()
        metric_reader = PeriodicExportingMetricReader(otlp_exporter)
        self.meter_provider = MeterProvider(resource=self.resource, metric_readers=[metric_reader])
        metrics.set_meter_provider(self.meter_provider)
        print(f"Metrics initialized for service: {self.service_name}")

    def initialize_logging(self):
        self.logger_provider = LoggerProvider(resource=self.resource)
        set_logger_provider(self.logger_provider)
        otlp_exporter = OTLPLogExporter()
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

        # Integrate with standard Python logging
        handler = LoggingHandler(level=logging.INFO, logger_provider=self.logger_provider)
        logging.getLogger().addHandler(handler)
        print(f"Logging initialized for service: {self.service_name}")

    def shutdown(self):
        if self.tracer_provider:
            self.tracer_provider.shutdown()
            print("TracerProvider shut down.")
        if self.meter_provider:
            self.meter_provider.shutdown()
            print("MeterProvider shut down.")
        if self.logger_provider:
            self.logger_provider.shutdown()
            print("LoggerProvider shut down.")

# Example Usage in your application's main entry point:
if __name__ == "__main__":
    telemetry_service = TelemetryService("my-application")

    # Initialize desired telemetry components
    telemetry_service.initialize_tracing()
    telemetry_service.initialize_metrics()
    telemetry_service.initialize_logging()

    # Get OpenTelemetry instruments
    tracer = trace.get_tracer(__name__)
    meter = metrics.get_meter(__name__)
    logger = logging.getLogger(__name__)

    # Example: Use telemetry in your application logic
    with tracer.start_as_current_span("main-application-flow"):
        logger.info("Application started.")
        counter = meter.create_counter("app_requests_total", description="Total application requests")
        counter.add(1)
        logger.warning("Something happened!")

    # Ensure telemetry is flushed before application exits
    telemetry_service.shutdown()
    print("Application finished and telemetry shut down.")
```

## Auto-Instrumentation for Web Frameworks

OpenTelemetry provides auto-instrumentation for many popular web frameworks, allowing you to automatically collect traces for incoming requests without manual code changes. This is particularly useful for quickly gaining visibility into your application's performance.

### Flask (Python) Auto-Instrumentation

To auto-instrument a Flask application, you'll use the `opentelemetry-instrumentation-flask` package and run your application with the `opentelemetry-instrument` command.

First, install the necessary packages:
```bash
pip install opentelemetry-distro opentelemetry-exporter-otlp flask opentelemetry-instrumentation-flask
```

Then, use `opentelemetry-bootstrap` to install other relevant instrumentation libraries:
```bash
opentelemetry-bootstrap -a install
```

Finally, run your Flask application using `opentelemetry-instrument`:
```bash
OTEL_SERVICE_NAME="my-flask-app" \
OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317" \
opentelemetry-instrument flask run -p 8080
```

Replace `flask run -p 8080` with the actual command you use to start your Flask application. You can configure the service name and OTLP exporter endpoint using environment variables.

**Important Considerations:**
*   Avoid running your Flask app in reloader or hot-reload mode (e.g., `flask run --reload`) when using OpenTelemetry auto-instrumentation, as it can break the instrumentation.
*   For more fine-grained control or custom telemetry, you can combine auto-instrumentation with manual instrumentation.

### Express (Node.js) Auto-Instrumentation

To auto-instrument an Express.js application, you'll use the `@opentelemetry/auto-instrumentations-node` package and configure the OpenTelemetry SDK to load these instrumentations.

First, install the necessary npm packages:
```bash
npm install --save @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-http
```

Create a separate file (e.g., `instrumentation.js`) for your OpenTelemetry setup. This file should be imported and run *before* your main Express application code.

`instrumentation.js`:
```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const traceExporter = new OTLPTraceExporter({
  // url: 'http://localhost:4318/v1/traces',
});

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'my-express-app',
  }),
  traceExporter: traceExporter,
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

console.log('OpenTelemetry SDK initialized.');

process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => console.log('OpenTelemetry SDK shut down successfully'))
    .catch((error) => console.log('Error shutting down OpenTelemetry SDK', error))
    .finally(() => process.exit(0));
});
```

Finally, run your Express application, ensuring `instrumentation.js` is loaded first:
```bash
node --require ./instrumentation.js app.js
```

Replace `app.js` with the path to your main Express application file. This will automatically instrument incoming HTTP requests and send traces to your configured OTLP endpoint.