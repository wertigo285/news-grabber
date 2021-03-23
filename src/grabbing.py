from graber.graber import SITES, Graber


def fill_news(base):
    sites = [site['name'] for site in SITES]
    grabber = Graber()
    for site in sites:
        site_grabber = getattr(grabber, site)
        last_date = base.get_last_news_date(site)
        newses = site_grabber.news(0, start_date=last_date)
        base.add(site, newses)
