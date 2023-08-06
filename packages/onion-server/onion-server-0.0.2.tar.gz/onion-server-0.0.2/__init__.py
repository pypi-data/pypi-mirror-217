from .onion_server import main

if __name__ == '__main__':
    # main()
    while True:
        action = main()
        if action != 'reboot':
            break
        