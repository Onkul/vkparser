import vk_api
import csv
import time

# Use your values
access_token = 'ADD YOUR VK ACCESS TOKEN'
owner_id = 'VK GROUP ID'
count = 100  # How many posts would be parsed (100 max per request)
csv_filename = 'post_info.csv'
offset = 74040  # Offset parameter, which is responsible for the range of messages to be parsed

# Convert a positive group_id value to a negative one to receive posts on behalf of the group
owner_id = f"-388266"

# Initializing the VK API session
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()

offset = 0  # Initializing the offset

while True:  # Infinite loop to automatically execute every 10 seconds
    # We get posts from a group starting from a certain offset and with the owner filter
    response = vk.wall.get(owner_id=owner_id, count=count, offset=offset, filter='owner')
    post_info = []

    for post in response['items']:
        post_id = post['id']

        post_text = post['text']
        likes_count = post['likes']['count']
        comments_count = post['comments']['count']

        # Getting author_id from the 'from_id' field of the post
        author_id = post['from_id']

        # We get the author's first and last name, if data is available
        user_info = vk.users.get(user_ids=author_id, fields=['first_name', 'last_name'])
        if user_info:
            author_name = f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
        else:
            author_name = "N/A"  # If author information is not available (that also means, a community publishes that post)

        post_info.append({'Post ID': post_id, 'Text': post_text, 'Likes': likes_count, 'Comments': comments_count,
                          'Author': author_name})

    # If there are new posts, add them to the CSV file
    if post_info:
        with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Post ID', 'Text', 'Likes', 'Comments', 'Author']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Checking whether headers need to be written to the CSV file (if the file is empty)
            if csvfile.tell() == 0:
                writer.writeheader()

            for post in post_info:
                writer.writerow(post)

        # Update offset for the next request
        offset += count

        print(f"Posts successfully gathered into '{csv_filename}'")

    # Delay 10 seconds before next execution
    time.sleep(10)