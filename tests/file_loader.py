
def read_fixtures_file(name):
    with open('tests/fixtures/' + name, 'r') as file:
        return file.read()
