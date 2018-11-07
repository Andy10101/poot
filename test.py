def f1(ss):
    print(ss)
    def f2():
        print(ss)
        def f3():
            print(ss)
        return f3

f1("ss")