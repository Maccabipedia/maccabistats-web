import os
import pickle

from dateutil import parser as date_parser
from flask import Flask, request, jsonify, session

from maccabistats.stats.serialized_games import get_maccabi_stats

app = Flask(__name__, static_folder="static-pages")
app.secret_key = "6"


def _remove_games_from_session():
    if 'pickled_game_path' in session:
        if os.path.exists(session['pickled_game_path']):
            os.remove(session['pickled_game_path'])
        session.pop("pickled_game_path", None)


@app.route("/")
def main_page():
    return app.send_static_file("stats.html")


@app.route("/api/stats", methods=["POST"])
def stats():

    games = get_maccabi_stats()

    games = filter_by_home_or_away(games, request.json['location'])
    games = filter_by_competition(games, request.json['competition'])
    games = filter_by_wins(games, request.json['only_wins'])
    games = filter_by_opponent(games, request.json['opponent'])
    games = filter_by_date(games, request.json['before_date'], request.json['after_date'])
    answer = "Maccabi Stats : {games}".format(games=repr(games))

    session['pickled_game_path'] = save_session_games_to_disk(games)

    print(request.json)
    return answer


@app.route("/api/opponents", methods=["GET"])
def get_opponents():
    g = get_maccabi_stats()
    return jsonify(list(g.available_opponents))


@app.route("/api/competitions", methods=["GET"])
def get_competitions():
    g = get_maccabi_stats()
    return jsonify(list(g.available_competitions))


@app.route("/api/best_scorers", methods=["GET"])
def get_best_scorers():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, goals=t[1]) for t in games.players.best_scorers])


@app.route("/api/best_assisters", methods=["GET"])
def get_best_assisters():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, assists=t[1]) for t in games.players.best_assisters])


@app.route("/api/most_yellow_carded", methods=["GET"])
def get_most_yellow_carded():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, yellow_cards=t[1]) for t in games.players.most_yellow_carded])


@app.route("/api/most_red_carded", methods=["GET"])
def get_most_red_carded():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, red_cards=t[1]) for t in games.players.most_red_carded])


@app.route("/api/most_substitute_off", methods=["GET"])
def get_most_substitute_off():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, subs_off=t[1]) for t in games.players.most_substitute_off])


@app.route("/api/most_substitute_in", methods=["GET"])
def get_most_substitute_in():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, subs_in=t[1]) for t in games.players.most_substitute_in])


@app.route("/api/most_lineup_players", methods=["GET"])
def get_most_lineup_players():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, lineup=t[1]) for t in games.players.most_lineup_players])


@app.route("/api/most_captains", methods=["GET"])
def get_most_captains():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, captain_times=t[1]) for t in games.players.most_captains])


@app.route("/api/most_penalty_missed", methods=["GET"])
def get_most_penalty_missed():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, penalty_missed=t[1]) for t in games.players.most_penalty_missed])


@app.route("/api/most_played", methods=["GET"])
def get_most_played():
    games = load_session_games_from_disk()
    return jsonify([dict(t[0].__dict__, played=t[1]) for t in games.players.most_played])


@app.route("/api/most_trained_coach", methods=["GET"])
def get_most_trained_coach():
    games = load_session_games_from_disk()
    return jsonify([dict(name=t[0], trained=t[1]) for t in games.coaches.most_trained_coach])


@app.route("/api/most_winner_coach", methods=["GET"])
def get_most_winner_coach():
    games = load_session_games_from_disk()
    return jsonify([dict(name=t[0], wins=t[1]) for t in games.coaches.most_winner_coach])


@app.route("/api/most_loser_coach", methods=["GET"])
def get_most_loser_coach():
    games = load_session_games_from_disk()
    return jsonify([dict(name=t[0], losses=t[1]) for t in games.coaches.most_loser_coach])


@app.route("/api/most_winner_coach_by_percentage", methods=["GET"])
def get_most_winner_coach_by_percentage():
    games = load_session_games_from_disk()
    most_winner_coach = []

    for item in games.coaches.most_winner_coach_by_percentage:
        name = item[0].split("-")[0].strip()
        games_trained = item[0].split("-")[1].strip()
        percentages = item[1]

        most_winner_coach.append(dict(name=name, gamess_trained=games_trained, wins_percentages=percentages))

    return jsonify(most_winner_coach)


@app.route("/api/most_loser_coach_by_percentage", methods=["GET"])
def get_most_loser_coach_by_percentage():
    games = load_session_games_from_disk()
    most_loser_coaches = []

    for item in games.coaches.most_loser_coach_by_percentage:
        name = item[0].split("-")[0].strip()
        games_trained = item[0].split("-")[1].strip()
        percentages = item[1]

        most_loser_coaches.append(dict(name=name, gamess_trained=games_trained, losses_percentages=percentages))

    return jsonify(most_loser_coaches)


@app.route("/api/longest_wins_streak_games", methods=["GET"])
def get_longest_wins_streak_games():
    games = load_session_games_from_disk()
    return jsonify([game.json_dict() for game in games.streaks.get_longest_wins_streak_games()])


@app.route("/api/longest_wins_streak_length", methods=["GET"])
def get_longest_wins_streak_length():
    games = load_session_games_from_disk()
    return jsonify(games.streaks.get_longest_wins_streak_length())


@app.route("/api/longest_unbeaten_streak_games", methods=["GET"])
def get_longest_unbeaten_streak_games():
    games = load_session_games_from_disk()
    return jsonify([game.json_dict() for game in games.streaks.get_longest_unbeaten_streak_games()])


@app.route("/api/longest_unbeaten_streak_length", methods=["GET"])
def get_longest_unbeaten_streak_length():
    games = load_session_games_from_disk()
    return jsonify(games.streaks.get_longest_unbeaten_streak_length())


@app.route("/api/longest_score_streak_games", methods=["GET"])
def get_longest_score_at_least_games():
    games = load_session_games_from_disk()
    return jsonify([game.json_dict() for game in games.streaks.get_longest_score_at_least_games(1)])


@app.route("/api/longest_score_streak_length", methods=["GET"])
def get_longest_score_streak_length():
    games = load_session_games_from_disk()
    return jsonify(games.streaks.get_longest_score_at_least_length(1))


@app.route("/api/longest_clean_sheet_streak_games", methods=["GET"])
def get_longest_clean_sheet_streak_games():
    games = load_session_games_from_disk()
    return jsonify([game.json_dict() for game in games.streaks.get_longest_clean_sheet_games()])


@app.route("/api/longest_clean_sheet_streak_length", methods=["GET"])
def get_longest_clean_sheet_streak_length():
    games = load_session_games_from_disk()
    return jsonify(games.streaks.get_longest_clean_sheet_length())


def filter_by_date(maccabi_games, before_date, after_date):
    parsed_before_date = date_parser.parse(before_date)
    parsed_after_date = date_parser.parse(after_date)

    date_format = "{day}.{month}.{year}"
    before_date_in_format = date_format.format(day=parsed_before_date.day, month=parsed_before_date.month,
                                               year=parsed_before_date.year)
    after_date_in_format = date_format.format(day=parsed_after_date.day, month=parsed_after_date.month,
                                              year=parsed_after_date.year)

    return maccabi_games.played_after(after_date_in_format).played_before(before_date_in_format)


def filter_by_wins(maccabi_games, only_wins):
    if only_wins:
        return maccabi_games.maccabi_wins
    else:
        return maccabi_games


def filter_by_opponent(maccabi_games, opponent):
    opponent = opponent.strip()
    if opponent == "הכל":
        return maccabi_games
    else:
        return maccabi_games.get_games_against_team(opponent)


def filter_by_competition(maccabi_games, competition):
    competition = competition.strip()
    if competition == "הכל":
        return maccabi_games
    elif competition == "ליגה ראשונה":
        return maccabi_games.get_first_league_games()
    else:
        return maccabi_games.get_games_by_competition(competition)


def filter_by_home_or_away(maccabi_games, location):
    if location == "הכל":
        return maccabi_games
    elif location == "בית":
        return maccabi_games.home_games
    elif location == "חוץ":
        return maccabi_games.away_games
    else:
        raise TypeError("location is : {location}".format(location=location))


def _get_games_full_file_path_for_this_session():
    games_file_name_for_this_session = "{ip}-games.maccabi".format(
        ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

    full_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session-games",
                                  games_file_name_for_this_session)

    return full_file_path


def save_session_games_to_disk(maccabi_games):
    """ Pickle the maccabi game to disk, Return the full pickled file path.
    :return: Pickled file path
    """

    full_file_path = _get_games_full_file_path_for_this_session()

    with open(full_file_path, 'wb') as f:
        pickle.dump(maccabi_games, f)

    return full_file_path


def load_session_games_from_disk():
    """
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """
    full_file_path = _get_games_full_file_path_for_this_session()

    with open(full_file_path, 'rb') as pickled_games:
        return pickle.load(pickled_games)

# if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True)
