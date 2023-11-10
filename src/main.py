from Site import Site


viewComics = Site("https://viewcomics.org/", "/comic-list?c=", 'a', 'big-link')
readComicOnline = Site("https://readcomiconline.li", "/ComicList?c=", 'a', None, "&page=")

viewComics.searchForComic("Invincible")
