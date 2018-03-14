# -*- coding: utf-8 -*-

import os
import pickle
import uuid
import time
import pprint

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


@app.route("/api/request", methods=["POST"])
def save_user_request():
    request_folder_path = os.path.dirname(os.path.abspath(__file__))

    random_file_name = uuid.uuid4().hex
    random_file_path = os.path.join(request_folder_path, "requests_from_site", random_file_name + ".txt")

    request.json['time'] = time.ctime()

    with open(random_file_path, 'w') as request_file:
        request_file.write(pprint.pformat(request.json))

    return jsonify("OK")


@app.route("/api/stats", methods=["POST"])
def stats():
    games = get_maccabi_stats()

    games = filter_by_home_or_away(games, request.json['location'])
    games = filter_by_competition(games, request.json['competition'])
    games = filter_by_opponent(games, request.json['opponent'])
    games = filter_by_stadium(games, request.json['stadium'])
    games = filter_by_coach(games, request.json['coach'])
    games = filter_by_referee(games, request.json['referee'])
    games = filter_by_player_name(games, request.json['player'])
    games = filter_by_wins(games, request.json['only_wins'])
    games = filter_by_date(games, request.json['before_date'], request.json['after_date'])
    answer = "Maccabi Stats : {games}".format(games=repr(games))

    session['pickled_game_path'] = save_session_games_to_disk(games)

    print(request.json)
    return answer


@app.route("/api/games", methods=["GET"])
def get_games():
    g = load_session_games_from_disk()
    return jsonify([game.json_dict() for game in g.games])


@app.route("/api/games_filters", methods=["GET"])
def get_games_filters():
    g = get_maccabi_stats()
    return jsonify(dict(
        opponents=g.available_opponents,
        coaches=g.available_coaches,
        referees=g.available_referees,
        competitions=g.available_competitions,
        stadiums=g.available_stadiums,
        players=list(set(player.name for player in g.available_players))
        # Set is to avoid dups in client side, list is to allow json it.
    ))


@app.route("/api/top_players_stats", methods=["GET"])
def get_top_players_stats():
    games = load_session_games_from_disk()
    minimum_games_required = 10

    return jsonify(dict(
        best_scorers=[dict(t[0].__dict__, goals=t[1]) for t in games.players.best_scorers],
        best_assisters=[dict(t[0].__dict__, assists=t[1]) for t in games.players.best_assisters],
        most_yellow_carded=[dict(t[0].__dict__, yellow_cards=t[1]) for t in games.players.most_yellow_carded],
        most_red_carded=[dict(t[0].__dict__, red_cards=t[1]) for t in games.players.most_red_carded],
        most_substitute_off=[dict(t[0].__dict__, subs_off=t[1]) for t in games.players.most_substitute_off],
        most_substitute_in=[dict(t[0].__dict__, subs_in=t[1]) for t in games.players.most_substitute_in],
        most_lineup=[dict(t[0].__dict__, lineup=t[1]) for t in games.players.most_lineup_players],
        most_captain=[dict(t[0].__dict__, captain_times=t[1]) for t in games.players.most_captains],
        most_penalty_missed=[dict(t[0].__dict__, penalty_missed=t[1]) for t in games.players.most_penalty_missed],
        most_played=[dict(t[0].__dict__, played=t[1]) for t in games.players.most_played],
        most_winners=[dict(t[0].__dict__, wins=t[1]) for t in games.players.most_winners],
        most_losers=[dict(t[0].__dict__, losses=t[1]) for t in games.players.most_losers],
        most_unbeaten=[dict(t[0].__dict__, unbeaten=t[1]) for t in games.players.most_unbeaten],
        most_clean_sheet=[dict(t[0].__dict__, clean_sheet=t[1]) for t in games.players.most_clean_sheet],
        most_winners_by_percentage=games.players.get_most_winners_by_percentage(minimum_games_required),
        most_losers_by_percentage=games.players.get_most_losers_by_percentage(minimum_games_required),
        most_unbeaten_by_percentage=games.players.get_most_unbeaten_by_percentage(minimum_games_required),
        most_clean_sheet_by_percentage=games.players.get_most_clean_sheet_by_percentage(minimum_games_required),))


@app.route("/api/top_coaches_stats", methods=["GET"])
def get_top_coaches_stats():
    games = load_session_games_from_disk()
    return jsonify(dict(
        most_trained=[dict(name=t[0], trained=t[1]) for t in games.coaches.most_trained_coach],
        most_winner=[dict(name=t[0], wins=t[1]) for t in games.coaches.most_winner_coach],
        most_loser=[dict(name=t[0], losses=t[1]) for t in games.coaches.most_loser_coach],
        most_winner_by_percentage=_get_most_winner_coach_by_percentage(),
        most_loser_by_percentage=_get_most_loser_coach_by_percentage()))


def _get_most_winner_coach_by_percentage():
    games = load_session_games_from_disk()
    most_winner_coach = []

    for item in games.coaches.most_winner_coach_by_percentage:
        name = item[0].split("-")[0].strip()
        games_trained = item[0].split("-")[1].strip()
        percentages = item[1]

        most_winner_coach.append(dict(name=name, games_trained=games_trained, wins_percentages=percentages))

    return most_winner_coach


def _get_most_loser_coach_by_percentage():
    games = load_session_games_from_disk()
    most_loser_coaches = []

    for item in games.coaches.most_loser_coach_by_percentage:
        name = item[0].split("-")[0].strip()
        games_trained = item[0].split("-")[1].strip()
        percentages = item[1]

        most_loser_coaches.append(dict(name=name, games_trained=games_trained, losses_percentages=percentages))

    return most_loser_coaches


@app.route("/api/top_referees_stats", methods=["GET"])
def get_top_referees_stats():
    games = load_session_games_from_disk()
    return jsonify(dict(
        most_judged=[dict(name=t[0], judged=t[1]) for t in games.referees.most_judged_referee],
        best_referee=[dict(name=t[0], wins=t[1]) for t in games.referees.best_referee],
        worst_referee=[dict(name=t[0], losses=t[1]) for t in games.referees.worst_referee],
        best_referee_by_percentage=_get_best_referee_by_percentage(),
        worst_referee_by_percentage=_get_worst_referee_by_percentage()))


def _get_best_referee_by_percentage():
    games = load_session_games_from_disk()
    best_referees = []

    for item in games.referees.best_referee_by_percentage:
        name = item[0].split("-")[0].strip()
        games_judged = item[0].split("-")[1].strip()
        percentages = item[1]

        best_referees.append(dict(name=name, games_judged=games_judged, wins_percentages=percentages))

    return best_referees


def _get_worst_referee_by_percentage():
    games = load_session_games_from_disk()
    worst_referee = []

    for item in games.referees.worst_referee_by_percentage:
        name = item[0].split("-")[0].strip()
        games_judged = item[0].split("-")[1].strip()
        percentages = item[1]

        worst_referee.append(dict(name=name, games_judged=games_judged, losses_percentages=percentages))

    return worst_referee


@app.route("/api/longest_streaks", methods=["GET"])
def get_longest_streaks():
    games = load_session_games_from_disk()
    return jsonify(dict(
        wins=[game.json_dict() for game in games.streaks.get_longest_wins_streak_games()],
        unbeaten=[game.json_dict() for game in games.streaks.get_longest_unbeaten_streak_games()],
        scored=[game.json_dict() for game in games.streaks.get_longest_score_at_least_games(1)],
        clean_sheet=[game.json_dict() for game in games.streaks.get_longest_clean_sheet_games()],
        goals_from_bench=[game.json_dict() for game in games.streaks.get_longest_goals_from_bench_games()],
        ties=[game.json_dict() for game in games.streaks.get_longest_ties_streak_games()]))


@app.route("/api/averages", methods=["GET"])
def get_average_goals_for_maccabi():
    games = load_session_games_from_disk()
    return jsonify(dict(goals_for_maccabi=games.averages.goals_for_maccabi,
                        goals_against_maccabi=games.averages.goals_against_maccabi))


@app.route("/api/results_summary", methods=["GET"])
def get_results_summary():
    games = load_session_games_from_disk()
    total_goals_for_maccabi = sum(game.maccabi_team.score for game in games)
    total_goals_against_maccabi = sum(game.not_maccabi_team.score for game in games)

    return jsonify(dict(wins_count=games.results.wins_count,
                        losses_count=games.results.losses_count,
                        ties_count=games.results.ties_count,
                        clean_sheet_count=len([1 for game in games if game.not_maccabi_team.score == 0]),
                        total_goals_for_maccabi=total_goals_for_maccabi,
                        total_goals_against_maccabi=total_goals_against_maccabi))


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
    if opponent == "All":
        return maccabi_games
    else:
        return maccabi_games.get_games_against_team(opponent)


def filter_by_stadium(maccabi_games, stadium):
    stadium = stadium.strip()
    if stadium == "All":
        return maccabi_games
    else:
        return maccabi_games.get_games_by_stadium(stadium)


def filter_by_coach(maccabi_games, coach):
    coach = coach.strip()
    if coach == "All":
        return maccabi_games
    else:
        return maccabi_games.get_games_by_coach(coach)


def filter_by_referee(maccabi_games, referee):
    referee = referee.strip()
    if referee == "All":
        return maccabi_games
    else:
        return maccabi_games.get_games_by_referee(referee)


def filter_by_player_name(maccabi_games, player_name):
    player_name = player_name.strip()
    if player_name == "All":
        return maccabi_games
    else:
        return maccabi_games.get_games_by_player_name(player_name)


def filter_by_competition(maccabi_games, competition):
    competition = competition.strip()
    if competition == "All":
        return maccabi_games
    elif competition == "ליגה ראשונה":
        return maccabi_games.get_first_league_games()
    else:
        return maccabi_games.get_games_by_competition(competition)


def filter_by_home_or_away(maccabi_games, location):
    if location == "All":
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
