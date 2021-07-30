Title: Top Posts with React and Pelican
Date: 2015-08-04 09:55
Category: Tech
Tags: scripting, python, pelican, javascript
Author: Ryan M
Status: draft

The majority of the traffic for this site comes via [this single post][sharedlinks]. I like to think that I have some other interesting things to say and thought about how I could suggest other articles to people visiting my site. My first attempt is by creating a "top posts this month" widget at the top of my blog using Pelican's plugin system, Piwik Analytics and React.
<!-- PELICAN_END_SUMMARY -->  

I've used Piwik as my site analytics for a while now. It's decent, open-source, and allows me to have full control over the analytics. I started poking around their API documentation and found that it's possible to pull analytics data to put on your site, but requires that you have a publicly accessible account that anyone could visit. I'm not okay with that for a lot of reasons. I realized recently that you can create your own widgets and segments within Piwik that also gives you an export option.  This export is simply a RESTful url which I realized I could take advantage of. Instead of exposing this to the public, I could run a script locally that would generate the data I need to display on my site. More on the url and how I pull the data later.

![piwik page views]({static}piwik_page_views.png)

There was one problem. The data returned from Piwik gives page views and urls, but no titles.

	:::python
    {
		u'avg_time_generation': 0.39,
		u'avg_time_on_page': 41,
		u'label': u'2013/11/03/dropboxsharedlinks/index',
		u'nb_hits': 10000000000000,
		u'nb_visits': 100000000000,
		...
		u'segment': u'pageUrl==http%3A%2F%2Fryanmo.co%2F2013%2F11%2F03%2Fdropboxsharedlinks%2F',
		u'url': u'http://ryanmo.co/2013/11/03/dropboxsharedlinks/'
	}

This is where Pelican's plugins comes in handy. I wrote a quick plugin that would output all of my articles in this format.

	:::python
	{
		"short_url": "2015/06/06/filling-forms-with-pdfpen-and-javascript", 
		"title": "Filling Forms with PDFPen and Javascript", 
		"full_url": "https://ryanmo.co/2015/06/06/filling-forms-with-pdfpen-and-javascript/", 
		"slug": "filling-forms-with-pdfpen-and-javascript"
	}

Now it's just a matter of combining the two pieces of information and then sorting by the number of views.

Pulling the information from my Piwik site was fairly straight forward

	:::python
	import datetime
	
    today = datetime.datetime.today()
    first_of_month = today.replace(day=1)

    # I use the previous month if it's before the 5th since there probably isn't enough traffic yet
    if today.day < 5:
        period = first_of_month.replace(month=(first_of_month.month - 1) or 12)
    else:
        period = first_of_month
    piwik_url = 'https://ryanmo.co/url_to_analytics'

	# This was from the export options on Piwik's site. 
	# I just cleaned up the url into a nice payload
    payload = {
        'module': 'API',
        'method': 'Actions.getPageUrls',
        'format': 'JSON',
        'idSite': '1',
        'period': 'month',
        'date': period.strftime('%Y-%m-%d'),
        'flat': '1',
        'segment': 'pageUrl!@.html',
        'token_auth': 'auth_token_for_my_site',
        'filter_limit': '100',
    }

    req = requests.get(piwik_url, params=payload)

    data = json.loads(req.text)

    # My segment didn't exclude the home page, so I exclude it
    data = [entry for entry in data if entry['url'] != 'http://ryanmo.co/']

	def remove_index(entry):
		"""
		Removes /index from the end of the label key so that
		the url matches the slug in all_articles.json
		"""
        if entry['label'] and entry['label'].endswith('/index'):
              entry['short_url'] = entry['label'].replace('/index', '')
	    return entry

    data = map(remove_index, data)


Generating a JSON file for all the articles on my site was easy to do in Pelican.

	:::python
    import os
    import json
    from pelican import signals

    class ArticlesJson(object):

        def __init__(self, generators, *args, **kwargs):
            self.articles = generators.articles
            self.settings = generators.settings

            self.contentpath = self.settings.get('PATH')
            self.siteurl = self.settings.get('SITEURL')
            self.output_path = os.path.join(self.contentpath, 'json')
            self.to_json = {'articles': []}
            self.file_name = '/all_articles.json'

        def write_json_to_file(self):
            self._ensure_path()
            with open(self.output_path + self.file_name, 'w') as f:
                json.dump(self.to_json, f, indent=4)

        def _ensure_path(self):
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)

        def generate_output(self):
            for article in self.articles:
                self.to_json['articles'].append(
                    dict(
                        full_url="%s/%s/" % (self.siteurl, article.url),
                        short_url="%s" % (article.url),
                        title=article.metadata.get('title'),
                        slug=article.slug,
                    )
                )
            self.write_json_to_file()

    def get_generators(generators):
        output = ArticlesJson(generators)
        output.generate_output()

    def register():
        signals.article_generator_finalized.connect(get_generators)

Now, let's combine the information from both of these pieces of data.

	:::python
    blog_path = os.path.join(
        os.path.join(os.path.dirname(__file__), os.pardir),
        'content',
    )
    
    json_path = os.path.join(blog_path, 'json')
    
    with open(os.path.join(json_path, 'all_articles.json')) as f:
        all_articles = json.loads(f.read()).get('articles')

    all_articles_urls = [article['short_url'] for article in all_articles]
    all_data_urls = [article['short_url'] for article in data]

    # The amount of data returned from Piwik doesn't always match the number
    # of articles on my blog. This reduces the posts to only those that were
    # returned from Piwik
    url_intersection = list(set(all_data_urls) & set(all_articles_urls))

    common_articles = [article for article in all_articles
                       if article['short_url'] in url_intersection]

    sorting_key = operator.itemgetter("short_url")

    for i, j in zip(
            sorted(common_articles, key=sorting_key),
            sorted(data, key=sorting_key)):
        j.update(i)

    sort_by_hits = sorted(data, key=lambda entry: entry['nb_hits'], reverse=True)
    top_five_articles = sort_by_hits[:5]

    def get_article_info(article):
        return {
            'title': article['title'],
            'url': article['full_url'],
            'slug': article['slug'],
        }

    to_ret = dict(
        period=period.strftime('%Y-%m-%d'),
        articles=map(get_article_info, top_five_articles)
        )

    with open(os.path.join(json_path, 'top_articles.json'), 'w') as w:
        json.dump(to_ret, w)

To keep the analytics information from being exposed publicly, I run the script as a cron once a day to update the top posts to my site and save it to my site's static path.

Now it's time to put it on the page. I've been enjoying learning React lately, so I took this as another opportunity to use React on my site to create a "Top Posts" widget on my site[^1]. 

	:::coffeescript
    d = React.DOM

    shuffle = (source) ->
      return source unless source.length >= 2

      for index in [source.length-1..1]
        randomIndex = Math.floor Math.random() * (index + 1)
        [source[index], source[randomIndex]] = [source[randomIndex], source[index]]
      source

    Post = React.createClass
      getInitialState: ->
        trackingCampaign =
          pk_campaign: 'Top-Posts'
          pk_kwd: @props.post.title.toLowerCase()
        trackingCampaignParams: @serialize trackingCampaign

      serialize: (obj) ->
        str = []
        for p of obj
          if obj.hasOwnProperty(p)
            str.push encodeURIComponent(p) + '=' + encodeURIComponent(obj[p])
        str.join '&'

      render: ->
        d.li {},
          d.span {},
            d.a {
              href: "#{@props.post.url}?#{@state.trackingCampaignParams}"
            }, @props.post.title

    Posts = React.createClass
      getInitialState: ->
        dataUrl: '/json/top_articles.json'
        articles: []

      componentDidMount: ->
        $.get @state.dataUrl, (result) =>
          if @isMounted
            @setState articles: shuffle(result.articles)

      render: ->
        d.div {id: "container"},
          d.header {}, "Popular Posts this Month"
          d.ul {},
            @state.articles.map (article) -> Post post: article

    $ ->
        top_posts = document.getElementById('top-posts')
        if document.location.pathname == '/' and top_posts
          React.render Posts({}), top_posts



sharedlinks: {static}/2013-11-03-dropboxsharedlinks.md
[^1]: I realized later that it looks a like like Brett Terpstra's widget at brettterpstra.com
