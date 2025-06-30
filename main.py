from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import requests
import matplotlib.pyplot as plt
import pandas as pd

def counter_most_commun(list):

    return Counter(list).most_common()


def get_biotools_total_count(api_url='https://bio.tools/api/tool/?format=json'):

    resp = requests.get(api_url, headers={'Accept': 'application/json'})
    resp.raise_for_status()
    return resp.json()['count']


def _fetch_status(url, timeout=2):

    try:
        resp = requests.get(url, timeout=timeout)
        return url, '404' if resp.status_code == 404 else '200'
    except requests.Timeout:
        return url, 'timeout'
    except Exception:
        return url, 'error'
    

def check_url(urls, timeout=2):

    results = [_fetch_status(url, timeout=timeout) for url in urls]
    return pd.DataFrame({'url': urls, 'result': results})




def check_url_parallel(urls, max_workers=20):

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch_status, url): url for url in urls}
        for future in as_completed(futures):
            url, status = future.result()
            results.append((url, status))
    return pd.DataFrame(results, columns=['url', 'result'])





def make_time_evolution_graph_per_year(date, title):

    import matplotlib.pyplot as plt
    from datetime import datetime
    from collections import Counter

    datetime_list = [datetime.fromisoformat(time[:-1]) for time in date]

    years = [dt.year for dt in datetime_list]
    yearly_counts = Counter(years)
    sorted_years, counts = zip(*sorted(yearly_counts.items()))

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_years, counts, marker='o', linestyle='-')

    plt.title(f'Number of {title} per Year')
    plt.xlabel('Year')
    plt.ylabel(f'Number of {title}')
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def create_dataframe(data):

    name = data['name']
    description = data['description']
    homepage = data['homepage']
    biotoolsID = data['biotoolsID']
    biotoolsCURIE = data['biotoolsCURIE']
    version = data['version']
    otherID = data['otherID']
    relation = data['relation']
    function = data['function']
    toolType = data['toolType']
    topic = data['topic']
    operatingSystem = data['operatingSystem']
    language = data['language']
    license = data['license']
    collectionID = data['collectionID']
    maturity = data['maturity']
    cost = data['cost']
    accessibility = data['accessibility']
    elixirPlatform = data['elixirPlatform']
    elixirNode = data['elixirNode']
    elixirCommunity = data['elixirCommunity']
    link = data['link']
    download = data['download']
    documentation = data['documentation']
    publication = data['publication']
    credit = data['credit']
    #community = data['community']
    owner = data['owner']
    additionDate = data['additionDate']
    lastUpdate = data['lastUpdate']
    editPermission = data['editPermission']
    validated = data['validated']
    homepage_status = data['homepage_status']
    elixir_badge = data['elixir_badge']
    confidence_flag = data['confidence_flag']

    df = pd.DataFrame({
        'name': [name],
        'description': [description],
        'homepage': [homepage],
        'biotoolsID': [biotoolsID],
        'biotoolsCURIE': [biotoolsCURIE],
        'version': [version],
        'otherID': [otherID],
        'relation': [relation],
        'function': [function],
        'toolType': [toolType],
        'topic': [topic],
        'operatingSystem': [operatingSystem],
        'language': [language],
        'license': [license],
        'collectionID': [collectionID],
        'maturity': [maturity],
        'cost': [cost],
        'accessibility': [accessibility],
        'elixirPlatform': [elixirPlatform],
        'elixirNode': [elixirNode],
        'elixirCommunity': [elixirCommunity],
        'link': [link],
        'download': [download],
        'documentation': [documentation],
        'publication': [publication],
        'credit': [credit],
        #'community': [community],
        'owner': [owner],
        'additionDate': [additionDate],
        'lastUpdate': [lastUpdate],
        'editPermission': [editPermission],
        'validated': [validated],
        'homepage_status': [homepage_status],
        'elixir_badge': [elixir_badge],
        'confidence_flag': [confidence_flag]
    })

    return df


def extract_all_data_sysbio():

    df = pd.DataFrame()

    num_page = 0
    num_tool = 0

    while True:

        num_page += 1
        url = f'https://bio.tools/api/tool?format=json&topic="Systems biology"&sort=additionDate&ord=asc&page={num_page}'
        response = requests.get(url)

        if response.status_code != 200:
            break

        content = response.json()

        for tool in content['list']:
            num_tool += 1
            df_ = create_dataframe(tool)
            df = pd.concat([df, df_], axis=0, ignore_index=True)

    return df

def extract_all_data(topic = 'Systems biology'):
    import pandas as pd
    import requests

    df = pd.DataFrame()

    num_page = 0
    num_tool = 0

    while True:

        num_page += 1
        url = f'https://bio.tools/api/tool?format=json&topic="{topic}"&sort=additionDate&ord=asc&page={num_page}'
        response = requests.get(url)

        if response.status_code != 200:
            break

        content = response.json()

        for tool in content['list']:
            num_tool += 1
            df_ = create_dataframe(tool)
            df = pd.concat([df, df_], axis=0, ignore_index=True)

    return df



def make_bar_graph(data, title, max_idx):

    data = [str(i) if i is not None else 'None' for i in data]


    top_20_topics, top_20_counts = zip(*counter_most_commun(data)[0:max_idx])

    plt.figure(figsize=(10, 6))
    plt.barh(top_20_topics, top_20_counts)

    plt.title(f'Top {max_idx} Most Common {title}')
    plt.xlabel('Number of Tools')
    plt.ylabel(f'{title}')
    plt.gca().invert_yaxis()
    plt.grid(True)

    for index, value in enumerate(top_20_counts):
        plt.text(value, index, str(value))

    plt.tight_layout()
    plt.show()


def mini_report(df_colum, most_common = True):

    print("-" * 60)
    print(f"Column name: {df_colum.name}")
    print("-" * 60)
    empty_tags = len(df_colum[df_colum.isna()]) + len(df_colum[df_colum.apply(lambda x: len(x) == 0)])


    print(f"Total number of tags: {len(df_colum) - empty_tags}")
    print(f"Number of empty tags: {empty_tags}")

    if len(df_colum[df_colum.isna()]) > 0:
        print(f"Percentage of empty tags: {empty_tags / len(df_colum) * 100:.2f}%")
    else:
        print(f"Percentage of empty tags: {empty_tags / len(df_colum) * 100:.2f}%")

    if len(df_colum[df_colum.isna()]) > 0:

        print(f"Number of unique tags: {len(df_colum.unique()) - 1}")
    else:
        try:
            print(f"Number of unique tags: {len(df_colum.unique())}")
        except:
            pass

    print("-" * 60)

    if most_common:

        print(f"Most common tags of {df_colum.value_counts().head(10)}")
