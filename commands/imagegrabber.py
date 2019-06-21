async def pixiv(message, api, os, discord):
    msplit = message.content.split()
    x = 0

    if len(msplit) == 1:
        msplit.append('day')
    elif msplit[1] == "help":
        await message.channel.send("**Usable modes:** ```day, week, month, day_male, day_female, week_original, "
                                   "week_rookie, day_r18, day_male_r18, day_female_r18, week_r18, week_r18g```")
        return 1

    # get ranking: 1-30
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    json_result = api.illust_ranking(msplit[1])
    print(json_result)

    try:
        print(json_result.illusts)
    except AttributeError:
        await message.channel.send(f"The flying fuck is {msplit[1]}? Use ``pixiv! help`` to see the available modes")
        return 1

    # download random illust in top 30 week rankings to 'dl' dir
    directory = "dl"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # while loop is for if the first 30 results all have blacklisted tags
    while True:
        notfound = True
        for count, illust in enumerate(json_result.illusts[x:]):
            if illust.type != "manga" and len(illust.meta_pages) == 0:
                tempillust = illust
                x = x + 1
                print(x)
                notfound = False
                break
        if notfound or x >= 29:
            print(json_result)
            x = 0
            next_qs = api.parse_qs(json_result.next_url)
            json_result = api.illust_ranking(**next_qs)
        else:
            # dl the illust
            illust = tempillust
            image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1]
            name = "illust_id_%d_%s_%s" % (illust.id, illust.title, extension)
            print(illust)
            if os.path.isfile(f"dl/{name}"):
                x = x + 1
                print(x)
            else:
                try:
                    api.download(image_url, path=directory, name=name)
                    f = open(f"dl/{name}", "rb")
                    outputfile = discord.File(fp=f)
                    await message.channel.send(
                        content=f"Source: <https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust.id}>",
                        file=outputfile)
                    return 0
                except:
                    x = x + 1


def danbooru(message, danb, oldposts):
    msplit = message.content.split()
    pg = 1
    tag = ["order:score", "rating:safe"]
    tag.extend(msplit[1:])

    stag = " ".join(tag)
    print(stag)
    while True:
        try:
            postlist = danb.post_list(limit=100, page=pg, tags=stag)
        except:
            return "U dun fucked up boi. Probably used more than one tag."
        if len(postlist) == 0:
            return "Tag not found. Try again?"
        for count, post in enumerate(postlist):
            if post['id'] in oldposts:
                continue
            else:
                oldposts.append(post['id'])
                try:
                    return post['large_file_url']
                except KeyError:
                    return post['file_url']
        pg = pg + 1


def reddit_get(message, reddit, oldsubmissions):
    msplit = message.content.split()

    if msplit[0] == "reddit!search":
        searchmode = True
    else:
        searchmode = False

    if len(msplit) <= 1:
        return "Usage: ``reddit! [subreddit] [hot/top/new/controversial] [timeframe for top]`` \nor ``reddit!search " \
               "[subreddit] [relevance/top/new] [search terms]``"

    subreddit = reddit.subreddit(msplit[1])

    # check if inputs are valid
    try:
        if subreddit != 'all':
            reddit.subreddits.search_by_name(subreddit, exact=True)
            subreddit.subreddit_type
    except:
        return "Not a valid subreddit."

    if searchmode:
        if len(msplit) > 2:
            if msplit[2] == 'relevance':
                submission_list = subreddit.search(query=" ".join(msplit[3:]))
            elif msplit[2] == 'top':
                submission_list = subreddit.search(query=" ".join(msplit[3:]), sort='top')
            elif msplit[2] == 'new':
                submission_list = subreddit.search(query=" ".join(msplit[3:]), sort='new')
            else:
                submission_list = subreddit.search(query=" ".join(msplit[2:]))
        else:
            submission_list = subreddit.search(query=" ".join(msplit[2:]))
    else:
        if len(msplit) > 2:
            if msplit[2] == 'hot':
                submission_list = subreddit.hot()
            elif msplit[2] == 'top':
                if len(msplit) > 3:
                    timeframe = msplit[3]
                else:
                    timeframe = 'day'
                try:
                    submission_list = subreddit.top(timeframe)
                except ValueError:
                    return "Not a valid timeframe."

            elif msplit[2] == 'new':
                submission_list = subreddit.new()
            elif msplit[2] == 'controversial':
                submission_list = subreddit.controversial()
            else:
                return "Not a valid sort type."
        else:
            submission_list = subreddit.hot()

    # go through submissions to find a suitable one
    for submission in submission_list:
        if not submission.is_self:
            if submission not in oldsubmissions:
                oldsubmissions.append(submission)
                return submission.url
    return "Either the subreddit only has text posts, or you've been calling the command too many times. Try a different" \
           " subreddit or sorting mode, or just wait a while."
