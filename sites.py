class Sites:
    def __init__(self):
        self.all_sites = []
        self.categories = set()

    def append_sites(self, name, sites):
        """Sites structured as (title, nickname, url)"""
        self.categories.add(name)
        for title, nickname, url in sites:
            print(title, nickname, url)
            if title and url:
                self.all_sites.append(Site(name, title, nickname, url))
            else:
                print(f'"{title}, {nickname}, {url}" is an invalid data entry')

    def display_sites(self):
        for site in self.all_sites:
            print(site)


class Site:
    def __init__(self, category, title, nickname, url):
        self.category = category
        self.title = title
        self.has_nickname = True if nickname is not None else False
        self.nickname = nickname
        self.url = url

    def __repr__(self):
        return f'Type: "{self.category}", Description: "{self.title}"{f", Nickname: {self.nickname}" * self.has_nickname}, Url: "{self.url}"'
