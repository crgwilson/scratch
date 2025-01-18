The Adapter is one of the [[Creational-Patterns]] described in [[Design Patterns Elements of Reusable Object-Oriented Software]].

Adapters are also known as "Wrapper".

Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

Use a Adapter when:

* You want to use an existing class, and its interface does not match the one you need.
* You want to create a reusable class that cooperates with unrelated or unforseen classes, that is, classes that don't necessarily have compatible interfaces.
* _(object adapter only)_ You need to use several existing subclasses, but it's impractical to adapt their interface by subclassing every one. An object adapter can adapt the interface of its parent class.

Class and Object Adapters have different trade-offs.

A Class Adapter will:

1. Adapt the Adaptee to Target by committing to a concrete Adapter class. As consequence, a class adapter won't work when we want to adapt a class _and_ all of its subclasses.
1. Lets Adapter override some of the Adaptee's behavior, since Adapter is a subclass of Adaptee.
1. Introduces only one object, and no additional pointer indirection is needed to get to the adaptee.

An Object Adapter will:

1. Let a single Adapter work with many Adaptees--that is, the Adaptee itself and all of its subclasses (if any). The Adapter can also add functionality to all Adaptees at once.
1. Make it harder to override Adaptee behavior. It will require subclassing the Adaptee and making the Adapter refer to the subclass rather than the Adaptee itself.

Implementation Techniques:

1. _Implementing class adapters in C++._ In a C++ implementation of a class adapter, Adapter would inherit publicly from Target and privately from Adaptee. Thus Adapter would be a subtype of Target but not of Adaptee.

Sample:

```cpp
class Shape {
public:
	Shape();
	virtual void BoundingBox(
		Point&, bottomLeft, Point& topRight
	) const;
	virtual Manipulator* CreateManipulator() const;
};

class TextView {
public:
	TextView();
	void GetOrigin(Coord& x, Coord& y) const;
	void GetExtent(Coord& width, Coord& height) const;
	virtual bool IsEmpty() const;
};

class TextShape : public Shape {
public:
	TextShape(TextView*);

	virtual void BoundingBox(
		Point& bottomLeft, Point& topRight
	) const;
	virtual bool IsEmpty() const;
	virtual Manipulator* CreateManipulator() const;

	TextShape::TextShape (TextView* t) {
		_text = t;
	}
};

void TextShape::BoundingBox (
	Point& bottomLeft, Point& topRight
) const {
	Coord bottom, left, width, height;

	_text->Getorigin(bottom, left);
	_text->GetExtent(width, height);

	bottomLeft = Point(bottom, left);
	topRight = Point(bottom = height, left + width);
}

bool TextShape::IsEmpty () const {
	return _text->IsEmpty();
}

Manipulator* TextShape::CreateManipulator () const {
	return new TextManipulator(this);
}
```

Related Patterns:

1. [[Bridge]] has a structure similar to an object adapter, but Bridge has a different intent: It is meant to separate an interface from its implementation so that they can be varied easily and independently. An adapter is meant to change the interface of an _existing_ object.
1. [[Decorator]] enhances another object without changing its interface. A decorator is thus more transparent to the application than an adapter is. As a consequence, Decorator supports recursive composition, which isn't possible with pure adapters.
1. [[Proxy]] defines a representative or surrogate for another object that does not change its interface.