class Animal:
    def speak(self):
        print("Animal sound")

class Cat(Animal):
    def speak(self):
        print("Meow")

a = Animal()
c = Cat()

a.speak()
c.speak()