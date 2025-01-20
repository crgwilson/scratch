The Bridge is one of the [[Creational-Patterns]] described in [[Design Patterns Elements of Reusable Object-Oriented Software]].

Bridges decouple an abstraction from its implementation so that the two can vary independently.

![[Bridge.png]]

Use a Bridge when:

* You want to avoid a permanent binding between an abstraction and its implementation. This might be the case, for example, when the implementation must be selected or switched at run-time.
* Both the abstractions and their implementations should be extensible by subclassing. In this case, the Bridge pattern lets you combine the different abstractions and implementations extend them independently.
* Changes in the implementation of an abstraction should have no impact on clients; that is, their code should not have to be recompiled.
* (C++) you want to hide the implementation of an abstraction completely from clients. In C++ the representation of a class is visible in the class interface.
* You have a proliferation of classes as shown earlier in the first Motivation diagram. Such a class hierarchy indicates the need for splitting an object into two parts. Rumbaugh uses the term "nested generalizations" to refer to such class hierarchies.

A Bridge will:

1. _Decoupling interface and implementation_. An implementation is not bound permanently to an interface. The implementation of an abstraction can be configured at run-time. It's even possible for an object to change its implementation at run-time. Decoupling abstraction and implementor also eliminates compile-time dependencies on the implementation. Changing an implementation class doesn't require recompiling the abstraction class and its clients. This property is essential when you must ensure binary compatibility between different versions of a class library. Furthermore, this decoupling encourages layering that can lead to a better structured system. The high-level part of a system only has to know about abstraction and implementor.
1. _Improved extensibility._ You can extend the abstraction and implementor hierarchies independently.
1. _Hiding implementation details from clients._ You can shield clients from implementation details, like the sharing of implementor objects and the accompanying reference count mechanism (if any).

Implementation Techniques:

1. _Only one Implementor._ In situations where there's only one implementation, creating an abstract implementor class isn't necessary. This is a degenerate case of the Bridge pattern; there's a one-to-one relationship between abstraction and implementor. Nevertheless, this separation is still useful when a change in the implementation of a class must not affect its existing clients-that is, they shouldn't have to be recompiled, just relinked.
2. _Creating the right implementor object._ How, when, and where do you decide which implementor class to instantiate when there's more than one?
	1. If abstraction knows about all ConcreteImplementor classes, then it can instantiate one of them in its constructor; it can decide between them based on parameters passed to its constructor.
	1. Another approach is to choose a default implementation initially and change it later according to usage.
	1. It's also possible to delegate the decision to another object altogether.
3. _Using multiple inheritance._ You can use multiple inheritance in C++ to combine an interface with its implementation. For example, a class can inherit publicly from abstraction and privately from a ConcreteImplementor. But because this approach relies on static inheritance, it binds an implementation permanently to its interface. Therefore you can't implement a true Bridge with multiple inheritance-at least not in C++.

Sample:

```cpp
class Window {
public:
	Window(View* contents);

	// requests handled by window
	virtual void Open();
	virtual void Close();
	virtual void Iconify();
	virtual void Deiconify();

	// requests forwarded to implementation
	virtual void SetOrigin(const Point& at);
	virtual void SetExtent(const Point& extent);
	virtual void Raise();
	virtual void Lower();

	virtual void DrawLine(const Point&, const Point&);
	virtual void DrawRect(const Point&, const Point&);
	virtual void DrawPolygon(const Point[], int n);
	virtual void DrawText(const char*, const Point&);

protected:
	WindowImp* GetWindowImp();
	View* GetView();

private:
	WindowImp* _imp;
	View* _contents; // the window's contents
};

class WindowImp {
public:
	virtual void ImpTop() = 0;
	virtual void ImpBottom() = 0;
	virtual void ImpSetExtent(const Point&)	 = 0;
	virtual void ImpSetOrigin(const Point&) = 0;

	virtual void DeviceRect(Coord, Coord, Coord, Coord) = 0;
	virtual void DeviceText(const char*, Coord, Coord) = 0;
	virtual void DeviceBitmap(const char*, Coord, Coord) = 0;
	// lots more functions for drawing on window...

protected:
	WindowImp();
};

class ApplicationWindow : public Window {
public:
	// ...
	virtual void DrawContents();
};

void ApplicationWindow::DrawContents () {
	GetView()->DrawOn(this);	
}

class IconWindow : public Window {
public:
	// ...
	virtual void DrawContents();
private:
	const char* _bitmapName;
};

void IconWindow::DrawContents() {
	WindowImp* imp = GetWindowImp();
	if (imp != 0) {
		imp->DeviceBitmap(_bitmapName, 0.0, 0.0);
	}
}

void Window::DrawRect (const Point& p1, const Point& p2) {
	WindowImp* imp = GetWindowImp();
	imp->DeviceRect(p1.X(), p1.Y(), p2.X(), p2.Y());
}

class XWindowImp : public WindowImp {
public:
	XWindowImp();

	virtual void DeviceRect(Coord, Coord, Coord, Coord);
	// remainder of the public interface...
private:
	// lots of X window system-specific state, including:
	Display* _dpy;
	Drawable _winid; // window id
	GC _gc;          // window graphic context
};

class PMWindowImp : public WindowImp {
public:
	PMWindowImp();
	virtual void DeviceRect(Coord, Coord, Coord, Coord);

	// remainder of public interface...
private:
	// lots of PM window system-specific state, including:
	HPS _hps;
};

void XWindowImp::DeviceRect (
	Coord x0, Coord y0, Coord x1, Coord y1
) {
	int x = round(min(x0, x1));
	int y = round(min(y0, y1));
	int w = round(abs(x0 - x1));
	int h = round(abs(y0 - y1));
	XDrawRectangle(_dpy, _winid, _gc, x, y, w, h);
}

void PMWindowImp::DeviceRect (
	Coord x0, Coord y0, Coord x1, Coord y1
) {
	Coord left = min(x0, x1);
	Coord right = max(x0, x1);
	Coord bottom = min(y0, y1);
	Coord top max(y0, y1);

	PPOINTL point[4];

	point[0].x = left;
	point[1].x = right;
	point[2].x = right;
	point[3].x = left;

	if (
		(GpiBeginPath(_hps, 1L) == false) ||
		(GpiSetCurrentPosition(_hps, &point[3]) == false) ||
		(GpiPolyLine(_hps, 4L, point) == GPI_ERROR) ||
		(GpiEndPath(_hps) == false)
	) {
		// report error
	} else {
		GpiStrokePath(_hps, 1L, 0L);
	}
}

WindowImp* Window::GetWindowImp () {
	if (_imp == 0) {
		_imp = WindowSystemFactory::Instance()->MakeWindowImp();
	}
	return _imp;
}
```

Related Patterns:

1. An [[Abstract-Factory]] can create and configure a particular Bridge.
2. The [[Adapter]] pattern is geared toward making unrelated classes work together. It is usually applied to systems after they're designed. Bridge, on the other hand, is used up-front in a design to let abstractions and implementations vary independently.