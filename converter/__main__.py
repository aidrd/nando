from .map import main as map_main
from .json2ttl import main as json2ttl_main

if __name__ == '__main__':
    print('map Nanbyo to Mondo')
    map_main('nanbyo')
    print('map Shoman to Mondo')
    map_main('shoman')
    print('convert ')
    json2ttl_main()



