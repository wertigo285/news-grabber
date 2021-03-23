from pprint import pprint

from graber.graber import SITES, Graber

if __name__ == '__main__':
    sites = [site['name'] for site in SITES]
    graber = Graber()
    for site in sites:
        parser = getattr(graber, site)
        news = parser.news(3)
        article = parser.grub(news[0]['link'])
        print(site)
        print('\n')
        pprint(news)
        print('\n')
        pprint(article)
        print('\n'*3)
