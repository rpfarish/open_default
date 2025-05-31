import webbrowser


class Sites:
    def __init__(self):
        self.all_sites: set[Site] = set()
        self.categories = set()

    def append_sites(self, category, sites):
        """Sites structured as (title, nickname, url)"""
        self.categories.add(category)
        for title, nickname, url in sites:
            if title and url:
                self.all_sites.add(Site(category, title, nickname, url))
            else:
                print(f'"{title}, {nickname}, {url}" is an invalid data entry')

    def display_sites(self):
        for site in self.all_sites:
            print(site)

    def call_all(self):
        for site in self.all_sites:
            webbrowser.open(site.url)

    def open_by_category(self, category: list[str]):
        for site in self.all_sites:
            sites = (set(site.sub_categories) & set(category))
            if site.has_nickname:
                sites |= (set(site.nickname) & set(category))
            for _ in sites:
                site.open()
        self.open_by_sub_category(category)

    def open_by_sub_category(self, category: list[str]):
        for i in category:
            for site in self.all_sites:
                if site.check_sub_category(i):
                    site.open()

    def open_by_nickname(self, category: list[str]):
        for i in category:
            for site in self.all_sites:
                if site.has_nickname and i == site.nickname:
                    site.open()

    def display_sites_by_sub_categories(self, category: list[str]):
        for i in category:
            for site in self.all_sites:
                if site.check_sub_category(i) or i in site.sub_categories or i == site.nickname:
                    print(site)

    def display_sites_by_category(self, category):
        for i in category:
            for site in self.all_sites:
                if site.check_sub_category(i):
                    print(site)

    def display_sites_by_nickname(self, name):
        for i in name:
            for site in self.all_sites:
                if site.has_nickname and i == site.nickname:
                    print(site)

    def display_categories(self):
        categories = {site.category for site in self.all_sites}
        for site in categories:
            print(site)


class Site:
    def __init__(self, category, title, nickname, url):
        self.category = category
        self.sub_categories = [i for i in self.category.split(":")]
        self.title = title
        self.has_nickname = True if nickname is not None else False
        self.nickname = nickname
        self.url = url

    def __repr__(self):
        return f'Category: "{self.category}", Description: "{self.title}"{f", Nickname: {self.nickname}" * self.has_nickname}, Url: "{self.url}"'

    def check_sub_category(self, category):
        partial_category = []
        for sub in self.sub_categories:
            partial_category.append(sub)
            if category == ':'.join(partial_category):
                return True
        else:
            return False

    def open(self):
        webbrowser.open(self.url)
