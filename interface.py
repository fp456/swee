import curses
from swe import Backend


def reset_screen(stdscr):
    stdscr.move(2, 0)
    stdscr.clrtobot()


def gety(stdscr):
    return stdscr.getyx()[0]


def getx(stdscr):
    return stdscr.getyx()[1]


def display_wrap(stdscr, s):
    for char in s:
        max_x = stdscr.getmaxyx()[1]
        if getx(stdscr) == max_x:
            stdscr.move(gety(stdscr)+1, 0)
        stdscr.addch(char)


def display_job_details(stdscr, job):
    title = job.get('title')
    company = job.get('company').get('display_name')
    location = job.get('location').get('display_name')
    description = job.get('description')
    link = job.get('redirect_url')
    reset_screen(stdscr)
    stdscr.addstr('Title: ')
    display_wrap(stdscr, title)
    stdscr.addstr(gety(stdscr) + 2, 0, 'Company: ')
    display_wrap(stdscr, company)
    stdscr.addstr(gety(stdscr) + 2, 0, 'Location: ')
    display_wrap(stdscr, location)
    stdscr.addstr(gety(stdscr) + 2, 0, 'Description: ')
    display_wrap(stdscr, description)
    stdscr.addstr(gety(stdscr) + 2, 0, 'Link: ')
    display_wrap(stdscr, link)


def display_ellipsis(stdscr, s, limit):
    for char in s:
        if getx(stdscr) == limit - 1:
            stdscr.addch('\u2026')
            return
        stdscr.addch(char)


def display_table(stdscr, table):
    stdscr.move(2, 2)
    stdscr.addstr('ID', curses.A_UNDERLINE)
    stdscr.move(2, 10)
    stdscr.addstr('Title', curses.A_UNDERLINE)
    stdscr.move(2, 50)
    stdscr.addstr('Company', curses.A_UNDERLINE)
    for i in range(len(table)):
        id = str(table[i].get('id'))
        stdscr.move(3 + i, 2)
        display_ellipsis(stdscr, id, 10)
        title = table[i].get('title')
        stdscr.move(3 + i, 10)
        display_ellipsis(stdscr, title, 50)
        company = table[i].get('company').get('display_name')
        stdscr.move(3 + i, 50)
        display_ellipsis(stdscr, company, stdscr.getmaxyx()[1])


def get_country(stdscr):
    countries_dict = {
        "1": "Austria",
        "2": "Brazil",
        "3":  "Canada",
        "4": "France",
        "5": "Germany",
        "6": "India",
        "7": "Italy",
        "8": "Netherlands",
        "9": "New Zealand",
        "10": "Poland",
        "11": "Russia",
        "12": "Singapore",
        "13": "South Africa",
        "14": "United Kingdom",
        "15": "United States",
    }
    stdscr.addstr('Enter country ID:\n')
    for id, country in countries_dict.items():
        stdscr.addstr(id + ": " + country + "\n")
    id = stdscr.getstr().decode(stdscr.encoding)
    stdscr.addstr('\n')
    while id not in countries_dict.keys():
        stdscr.move(gety(stdscr)-2, 0)
        stdscr.clrtobot()
        stdscr.addstr('Please enter a valid input\n')
        stdscr.addstr(id+'\n')
        id = stdscr.getstr().decode(stdscr.encoding)
    return id


def get_valid_input(stdscr, accepted_inputs):
    input = stdscr.getkey()
    while input not in accepted_inputs:
        stdscr.addstr('Please enter a valid input\r')
        input = stdscr.getkey()
    return input


def main(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr('You are in the main menu.\n\n'
                      'Press s to search jobs.\n'
                      'Press v to view saved jobs.\n'
                      'Press q to quit.\n')
        input = get_valid_input(stdscr, ['s', 'v', 'q'])
        if input == 's':
            search(stdscr)
        elif input == 'v':
            saved_jobs(stdscr)
        elif input == 'q':
            return


def search(stdscr):
    stdscr.clear()
    stdscr.addstr('You are in search.')
    curses.echo()
    reset_screen(stdscr)
    # stdscr.addstr(2,0,'Enter a keyword to search: ')
    # keyword = stdscr.getstr().decode(stdscr.encoding)
    country = get_country(stdscr)
    reset_screen(stdscr)
    stdscr.addstr('Enter a location: ')
    location = stdscr.getstr().decode(stdscr.encoding)
    curses.noecho()
    backend = Backend(country, location)
    while True:
        job = backend.next_job()
        display_job_details(stdscr, job)
        y = stdscr.getyx()[0]
        stdscr.addstr(y+2, 0, 'Press n to go to the next job.\n'
                              'Press s to save this job.\n'
                              'Press m to return to the main menu.\n')
        input = get_valid_input(stdscr, ['n', 's', 'm'])
        if input == 's':
            save_job(job)  # dummy

        elif input == 'm':
            return


def saved_jobs(stdscr):
    stdscr.clear()
    stdscr.addstr('You are in your saved jobs.')
    saved = get_saved_jobs()  # dummy
    page = 0
    while True:
        reset_screen(stdscr)
        start = 5 * page
        end = start + 5
        if end >= len(saved):
            end = len(saved)
        display_table(stdscr, saved[start:end])
        y = stdscr.getyx()[0]
        stdscr.move(y+2, 0)
        prompt = 'Press v to view a job.\n' \
                 'Press d to delete a job.\n'
        accepted_inputs = ['v', 'd', 'm']
        if end < len(saved):
            prompt += 'Press n to go to the next page.\n'
            accepted_inputs.append('n')
        if start > 0:
            prompt += 'Press p to go to the previous page.\n'
            accepted_inputs.append('p')
        prompt += 'Press m to return to the main menu.\n'
        stdscr.addstr(prompt)
        input = get_valid_input(stdscr, accepted_inputs)
        if input == 'v':
            curses.echo()
            stdscr.addstr('Enter the id of the job you\'d like to view: ')
            id = stdscr.getstr().decode(stdscr.encoding)
            curses.noecho()
            job = get_job(id)  # dummy
            display_job_details(stdscr, job)
            y = stdscr.getyx()[0]
            stdscr.addstr(y+2, 0, 'Press r to return.\n')
            get_valid_input(stdscr, ['r'])
        elif input == 'd':
            curses.echo()
            stdscr.addstr('Enter the id of the job you\'d like to remove: ')
            id = stdscr.getstr().decode(stdscr.encoding)
            curses.noecho()
            delete_job(id)  # dummy
        elif input == 'n':
            page += 1
        elif input == 'p':
            page -= 1
        elif input == 'm':
            return

# Dummy functions


def save_job(job_info):
    pass


def get_saved_jobs():
    result = []
    for i in range(20):
        template = {
            'title': 'Software Engineer - Internship',
            'company': {'display_name': 'Multiply Labs'},
            'location': {'display_name': 'San Francisco, California'},
            'description': 'About Multiply Labs At Multiply Labs, our mi...',
            'redirect_url': 'https://www.adzuna.com/land/ad/3226294323?se...'
        }
        template['id'] = i
        result.append(template)
    return result


def get_job(id):
    return {'title': 'Software Engineer - Internship',
            'company': {'display_name': 'Multiply Labs'},
            'location': {'display_name': 'San Francisco, California'},
            'description': 'About Multiply Labs At Multiply Labs, our mi...',
            'redirect_url': 'https://www.adzuna.com/land/ad/3226294323?se...'}


def delete_job(id):
    pass


if __name__ == '__main__':
    curses.wrapper(main)
