

def save_image(buf, file="test.jpeg"):

    try:
        with open(file, "wb") as f:
            f.write(buf)
    except OSError as e:
        print("exception .. {}".format(e))

    print(file)
