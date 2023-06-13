import urllib.parse as urlparse

from api import constants


def add_paging_to_response(request, response, query_data, page, total_pages):
    url = request.build_absolute_uri()

    if query_data.has_next():
        response[constants.HEADER_NEXT] = replace_page_param(url, query_data.next_page_number())
    if query_data.has_previous():
        response[constants.HEADER_PREV] = replace_page_param(url, query_data.previous_page_number())
    
    if page < total_pages and (query_data.has_next() and query_data.next_page_number() != total_pages):
        response[constants.HEADER_LAST] = replace_page_param(url, total_pages)
    if page > 1 and (query_data.has_previous() and query_data.previous_page_number() != 1):
        response[constants.HEADER_FIRST] = replace_page_param(url, 1)

    return response

def replace_page_param(url, new_page):
    parsed = urlparse.urlparse(url)

    querys = parsed.query.split("&")

    has_page = False

    for e in querys:
        if e.split("=")[0] == "p":
            e = "p=" + str(new_page)
            has_page = True
    
    if not has_page:
        querys.append("p=" + str(new_page))

    new_query = "&".join(["{}".format(query) for query in querys])
    
    parsed = parsed._replace(query=new_query)

    return urlparse.urlunparse(parsed)


