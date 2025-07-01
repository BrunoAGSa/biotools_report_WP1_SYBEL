from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import pandas as pd

API_URL = "https://bio.tools/api/tool/"


def counter_most_common(list_):
    return Counter(list_).most_common()


def get_biotools_total_count(api_url=None, timeout=2):

    if api_url is None:
        api_url = API_URL

    resp = requests.get(f"{api_url}?format=json",
                        headers={'Accept': 'application/json'},
                        timeout=timeout)
    resp.raise_for_status()
    return resp.json()['count']


def _fetch_status(url, timeout=2):

    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code
    except requests.Timeout:
        return 'timeout'
    except Exception as err:
        # print(f"Error fetching {url}: {err}")
        return 'error'


def check_urls(urls, timeout=2):
    results = [(url, _fetch_status(url, timeout=timeout)) for url in urls]
    return pd.DataFrame({'url': urls, 'result': results})


def check_urls_parallel(urls, max_workers=20):

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(_fetch_status, url): url
            for url in urls
        }
        for future in as_completed(future_to_url):
            results.append((future_to_url[future], future.result()))
    return pd.DataFrame(results, columns=['url', 'result'])


def make_time_evolution_graph_per_year(date, title):

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
    df = pd.DataFrame(data['list'])
    return df


def extract_all_data_sysbio(api_url=None, timeout=2):

    if api_url is None:
        api_url = API_URL

    df = pd.DataFrame()

    num_page = 0
    num_tool = 0

    while True:

        num_page += 1
        url = f'{api_url}?format=json&topic="Systems biology"&sort=additionDate&ord=asc&page={num_page}'
        response = requests.get(url, timeout=timeout)

        if response.status_code != 200:
            break

        content = response.json()

        for tool in content['list']:
            num_tool += 1
            df_ = create_dataframe(tool)
            df = pd.concat([df, df_], axis=0, ignore_index=True)

    return df


def extract_all_data(topic='Systems biology', api_url=None, max_pages=None):

    if api_url is None:
        api_url = API_URL

    dfs = []

    num_page = 0
    num_tool = 0
    page_arg = "page=1"

    # print("Downloading tool data...")
    sess = requests.Session()

    while True:

        # print(f"On page: {num_page}")
        url = f'{api_url}?format=json&topic="{topic}"&sort=additionDate&ord=asc&{page_arg}'
        response = sess.get(url)

        if response.status_code != 200:
            # print("Bad response! Stopping here.")
            break

        content = response.json()

        df = create_dataframe(content)
        num_tool += df.shape[0]
        dfs.append(df)
        num_page += 1

        if max_pages is not None and num_page >= max_pages:
            # print(f"Reached max pages: {max_pages}. Stopping here.")
            break

        next_page = content["next"]
        if next_page is None:
            break
        page_arg = next_page[1:]

    df = pd.concat(dfs, axis=0, ignore_index=True)
    # print("Done downloading tool data.")
    # print(f"Parsed {num_tool} tools from {num_page} pages.")

    # remove all newlines
    df = df.replace(r'\n',' ', regex=True)

    return df


def make_bar_graph(data, title, max_idx):

    data = [str(i) if i is not None else 'None' for i in data]

    if len(data) == 0:
        print("No data to plot.")
        return

    top_20_topics, top_20_counts = zip(*counter_most_common(data)[0:max_idx])

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


def mini_report(df_colum, most_common=True):

    print("-" * 60)
    print(f"Column name: {df_colum.name}")
    print("-" * 60)
    empty_tags = len(df_colum[df_colum.isna()]) + len(
        df_colum[df_colum.apply(lambda x: len(x) == 0)])

    print(f"Total number of tags: {len(df_colum) - empty_tags}")
    print(f"Number of empty tags: {empty_tags}")

    if len(df_colum[df_colum.isna()]) > 0:
        print(
            f"Percentage of empty tags: {empty_tags / len(df_colum) * 100:.2f}%"
        )
    else:
        print(
            f"Percentage of empty tags: {empty_tags / len(df_colum) * 100:.2f}%"
        )

    if len(df_colum[df_colum.isna()]) > 0:
        print(f"Number of unique tags: {len(df_colum.unique()) - 1}")
    else:
        try:
            print(f"Number of unique tags: {len(df_colum.unique())}")
        except Exception as err:
            # print(f"Error calculating unique tags: {err}")
            pass

    print("-" * 60)

    if most_common:
        print(f"Most common tags of {df_colum.value_counts().head(10)}")
