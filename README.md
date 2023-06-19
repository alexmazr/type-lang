# type-lang
Type is currently a fictional, but statically and strongly typed, semi-manually memory managed language. It's meant to be inspired by a slew of languages I've used over the years 
like Zig, Rust, Ada, and a few more. I don't have any lofty goals with Type, it's just a good personal project. That said, here is "milestone" checklist
I've come up with for Type that I intend to meet:
- [] All v0 language features implemented
- [] Bootstrap
- [] A relatively complex project: A multithreaded HTTP webserver
I expect this will take me a long time.


## type overview
This section is going to be a living document describing in detail what the syntax of the language is, how it will behave, and what features might ship
in the std. Not everything is set in stone.


### hello world
Let's start with a basic hello world. All Type programs must start with a `main` function. Type will also have `print` and `input` in the std, and
will be automatically imported. Here's an example:
```
fn main() {
  string name = input("What's your name?");
  print("hello {name}");
}
```
Pretty straightforward. I said that Type is semi-manually memory managed, so I'll describe what's happening briefly, and we'll get more into detail later.
The `input` function will prompt a user for their name, allocate some memory, and pass ownership back to `main`. The String `name` will get free'd at the end
of `main` unless another function takes ownership. Technically `name` is a pointer, but pointers are always dereferenced automatically when read or written to
in Type. All variables are immutable by default in Type. However they can be changed by annotating types with the `mut` keyboard:
```
fn main() {
  mut string name = input("What's your name?");
  name = "psych";
  print("hello {name});
}
```

### the type system
Funnily enough the type language spec doesn't contain any seriously useful types. It does however contain a set of what I'm calling "representational types".
These are types that can be to specify the underlying representation of a type, either to the compiler or natively. Type has the following representational types,
note though that type has "hidden" types that you can't extend, but can syntactially create, we'll visit those later though:
- `unsigned`
- `signed`
- `float`
- `list`
- `map`
- `range`
- `enum`
- `record`
- `interface`
- `error`
- `optional`
These types server as the foundation for the Type type system. But wait... didn't you use a `string` earlier? But `string` is missing? Indeed it is. That's
because `String` will be included in the std, along with some common types like `u8`, `i32`, `f64`, `bool`, `char` etc. Let's see how we can define some of those
below:
```
type u8 is unsigned<8>; // defines an unsigned 8 bit integer
type i32 is signed<32>; // defines a signed 32 bit integer
type f64 is float<64>; // defined a 64 bit IEEE754 float (might add a float standard option)
type bool is enum {    // defines an enum called bool
  true,
  false
}
type char is unsigned<32>; // char is 4 bytes because it's meant to store a unicode character
type string is list<char, i32>; // string is a list of chars with an iterator of type i32
```
Since `string` is really just a list of `char`, and `char` is really just an `unsigned<32>`, type provides some syntactic sugar for dealing with `string`'s in
the form of string-literals. Just like every other language you can surround some words in quotes and the type compiler will match expect that they're to be
stored in a list of `unsigned`.

We can also attach functions to types! Let's look at the `bool` enum:
```
type bool is enum {
  true,
  false;
  
  fn flip() self {
    return match self {
      true -> false;
      false -> true;
    }
  }
}
```

Let's look at some more types. We can start with `range`. There isn't a `range` keyword in type, just some special syntax, it looks like the following:
```
type floors is 0 .. 10;
```
The above defines a type called `floors` that will be binned into `unsinged<8>` automatically. Whenever `floors` is assigned runtime checks will be inserted
such that whenever you read `floors` it will always have a value between 0 and 10 inclusive. We can also use ranges on enums:
```
type day is enum {
  Monday, Tuesday, Wednesady, Thursday, Friday, Saturday, Sunday
}
type weekday is day where Monday .. Friday;
```
We defined a type `day` that contains all the days of the week, then specified a derived type `weekday` from `day` with a range on the possible days.
The `where` keyword is new, but basically it allows subset expressions on types. It also shares any functions
on day. We only need to use `where` when making strict subset types, if we want a simple type alias we can do the following:
```
type byte is u8;
```
We can subset types in other ways besides ranges. A `where` clause on a type can be used to add a complex expression as an invariant.
```
type ValidExtension is string 
  where self == "yml" or self == "json" or self == "xml";
```
Let's show an example of us using this type:
```
fn main() {
  string ext = ...;
  match ext {
    ValidExtension vext -> print("{vext} is valid!");
    _ -> print("invalid");
  }
}
```
This shows a pretty cool example. We defined in our type system what valid extensions are. We said they're a string, and that they must meet a specific condition.
In type `match` can use the type system to pattern match and cast your type up from a base type.

Let's finally look at `record`'s.
```
type shape is interface {
  fn area() u32;
}
```
Here we can define an interface that has a single functional interface. Any type that's created from `shape` will have to implement any functional interfaces defined
in `shape`. In this case it's just `area`. Let's create a rectangle:
```
final type rectangle is record<shape> {
  u32 length;
  u32 width;
  
  fn area() u32 {
    return self.l1 * self.l2;
  }
}
```
A `record` must define all members at the top, then it can define it's functions (or functional interfaces). Rectangle can also define functional
interfaces. We can also append the `final` keyword to any type to disallow type extension. Fields in records are private by default, but we can
mark types with `pub` to make them public. This is advised over getters/setters. Let's use our rectangle:
```
fn main() {
  shape unknown = rectangle(20, 10);
  match unknown {
    rectangle rect -> print("rect has area {rect.area()});
    _ -> print("unknown shape!");
  }
  print("unknown has area {unknown.area()});
}
```
Type has two more types `error`, and `optional`. The `error` type can be used as follows:
```
type NetworkError is error;

fn ping(sting address) string! { ... }
```
Here we have a `NetworkError` type, and a `ping` method. While I haven't written out the full method we can assume that `ping` could RETURN a `NetworkError`.
The exclamation mark is a way of saying "this function could return a string or an error". We can handle the possibility of an error in a couple of different
ways. Let's look at `match` first:
```
fn main() {
  match ping("8.8.8.8") {
    string resp -> ...;
    NetworkError e -> print("uh oh");
  }
}
```
Type can also `panic`, and it will terminate the current process or thread. There is no "catching" a `panic` in type.
```
fn main() {
  string resp = try ping("8.8.8.8");
}
```
The `try` keyword will `panic` if the return type from `ping` is an error. 

Type also has optional types!
```
fn getUser(UserId uid) User? { ... }
```
Optional types can be used in a match like so:
```
fn main() {
  match getUser(uid) {
    User user -> ...;
    Empty -> print("no user :(");
  }
}
```
Optional types can be combined with error types like so:
```
fn getUser*=(UserId uid) User?! { ... }
```
The order of the ? and ! do not matter. This will always result in an `enum` type like:
```
... enum {
  optional<User>,
  error
}
```
And btw, any `enum` type that contains any `error` type can be "tried" (`try myEnum`) to coerce a `panic` if that enum is an error type.

Map type:
```
type JsonVal is enum {
  true,
  false,
  null,
  String s,
  
}
type JsonMap is map<String, JsonVal>;
type Map<K, V> is map<K, V>;

fn main() {
  map d = {"hello": 23};
  // could be mut map as well
  Map d = new {};
  
  
}


```

### types and memory
Type is semi-manually memory managed. By that I mean you won't see the words `malloc` or `free`, but you will have to think about memory and the rules
of types memory system (much like Rust). In type memory can be allocated using the `new` keyword. This essentially denotes that a value should live
on the heap, and for `list`'s it will make them dynamic. Let's look at an exmaple:
```
type Event is enum {
  Create,
  Update,
  Delete
}
type Events is list<Event, u32>;

fn main() {
  mut Events events = new [100];
  ...
}
```
We create a mutable list of events, use new to make it dynamic, and give it an initial capacity of 100. If we add more than 100 events to the list then
events will allocate itself more memory. If we wanted to share the list of events across threads then we will use `shared` instead of `new`. The rule
for freeing memory is simple, it's free'd at the end of the function where ever it was declared (except for shared, it's free'd when the last function that's
using it ends). This is super limited, and so type provides a way to transfer ownership between functions. Let's take a look at the function definition for 
the `input` function we used in the hello world example:
```
fn input(string prompt) give string { ... }
```
Functions in type have three main parts of their type contract: arguments, parameters, and return types. Arguments are what are passed into functions,
parameters are part of the function definition and define the types of arguments expected. Return types define the type the function will return.
Arguments and return types can be marked with the `give` keyword, and parameters can be maked with the `take` keyword. The `give` keyword is saying
"I am giving you ownership", while the `take` keyword says "I am taking ownership". Let's look at some examples:
```
fn main() {
  string name = new "alex";
  sayHello(give name);
  print("hello again {name}");
}

fn sayHello(take string name) {
  print("hello {name}");
}
```
The above example will fail to compile, name was taken by `sayHello`, and also given by `main`. So when `main` tried to use `name` again it was already freed
by `sayHello`.























