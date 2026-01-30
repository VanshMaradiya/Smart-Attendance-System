from auth import register_user


def main():
    username = "Vansh"
    password = "admin123"
    role = "admin"
    name = "Admin"

    ok, msg = register_user(username, password, role, name)
    print(msg)

    if ok:
        print(f" Admin created successfully!")
        print(f" Username: {username}")
        print(f" Password: {password}")
    else:
        print(" Admin already exists or error occurred.")


if __name__ == "__main__":
    main()
