def load_status_closure(status_collection, user_collection):
    verified_users = []

    def inner_function(reader):
        for row in reader:
            user_id = row['USER_ID']
            valid_user = False

            # if user_id in verified_users list.
            if user_id in verified_users:
                valid_user = True

            # else query user_collection model to see if id exists
            else:
                query = user_collection.find_one(user_id=user_id)
                if query:
                    # add ID to verified_users
                    verified_users.append(user_id)
                    valid_user = True

            # if user id is valid user add to status_collection model
            if valid_user:
                try:
                    status_collection.insert(
                        user_id=row['USER_ID'],
                        status_id=row['STATUS_ID'],
                        status_text=row['STATUS_TEXT'])
                except pw.IntegrityError:
                    return False
            # else user ID not in user_collection dont add to status_collection
            else:
                return False
        # print(verified_users)
        return True
    return inner_function


def load_status_updates(filename, status_collection, user_collection):
    '''
        Opens a CSV file with user data and loads it to a SQL database.
    '''
    cwd = os.getcwd()
    try:
        with open((cwd + "/" + filename + ".csv"), newline='') as status_csv:
            reader = csv.DictReader(status_csv)

            # create instance of closure
            add_records = load_status_closure(status_collection, user_collection)
            return add_records(reader)
    except (FileNotFoundError, IOError):
        print('Error: File not found')
        return False
    return True
