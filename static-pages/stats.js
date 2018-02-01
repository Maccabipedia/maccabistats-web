var app = angular.module('MaccabiStatsApp', ['angularUtils.directives.dirPagination']);
app.controller('MaccabiStatsController', function ($scope, $http) {

    $scope.All = "הכל";
    $scope.firstLeague = "ליגה ראשונה";
    $scope.LocationOptions = ["בית", "חוץ"];
    $scope.OnlyWins = false;
    $scope.AfterDate = new Date("1900");
    $scope.BeforeDate = new Date();
    $scope.Competition = $scope.All;
    $scope.limit = 10;

    $scope.getstats = function () {

        // Remove current stats
        $scope.filteredGames = undefined;

        $scope.topPlayersStats = undefined;
        $scope.topCoachesStats = undefined;
        $scope.longestStreaks = undefined;

        $scope.averages = undefined;
        $scope.resultsSummary = undefined;


        data = {
            opponent: $scope.SelectedOpponent.trim(),
            location: $scope.SelectedLocation.trim(),
            stadium: $scope.SelectedStadium.trim(),
            player: $scope.SelectedPlayer.trim(),
            referee: $scope.SelectedReferee.trim(),
            coach: $scope.SelectedCoach.trim(),
            competition: $scope.SelectedCompetition.trim(),
            before_date: $scope.BeforeDate,
            after_date: $scope.AfterDate,
            only_wins: $scope.OnlyWins
        };
        console.log(data);
        $http({
            method: 'POST',
            data: data,
            url: '/api/stats'
        }).then(function successCallback(response) {
            $scope.msg = response.data;
            console.log(response.data);
            
            // Get the new stats from the server
            $scope.getFilteredGames();

            $scope.getTopPlayersStats();
            $scope.getCoachesStats();
            $scope.getLongestStreaks();

            $scope.getAverages();
            $scope.getResultsSummary();

        }, function errorCallback(response) {
            $scope.msg = "server error";
        });
    };

    $scope.getAvailableGameFilterOptions = function () {
        $http({
            method: 'GET',
            url: '/api/games_filters'
        }).then(function successCallback(response) {

            $scope.gameFilters = response.data;
            $scope.AvailableOpponents = $scope.gameFilters.opponents;
            $scope.AvailableOpponents.push($scope.All);

            $scope.AvailableCoaches = $scope.gameFilters.coaches;
            $scope.AvailableCoaches.push($scope.All);

            $scope.AvailableReferees = $scope.gameFilters.referees;
            $scope.AvailableReferees.push($scope.All);

            $scope.AvailableCompetitions = $scope.gameFilters.competitions;
            $scope.AvailableCompetitions.push($scope.All);
            $scope.AvailableCompetitions.push($scope.firstLeague);

            $scope.AvailableStadiums = $scope.gameFilters.stadiums;
            $scope.AvailableStadiums.push($scope.All);

            $scope.AvailablePlayers = $scope.gameFilters.players;
            $scope.AvailablePlayers.push($scope.All);

            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getFilteredGames = function () {
        $http({
            method: 'GET',
            url: '/api/games'
        }).then(function successCallback(response) {
            $scope.filteredGames = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getTopPlayersStats = function () {
        $http({
            method: 'GET',
            url: '/api/top_players_stats'
        }).then(function successCallback(response) {
            $scope.topPlayersStats = response.data;

            $scope.bestScorers = $scope.topPlayersStats.best_scorers;
            $scope.bestAssisters = $scope.topPlayersStats.best_assisters;
            $scope.mostYellowCarded = $scope.topPlayersStats.most_yellow_carded;
            $scope.mostRedCarded = $scope.topPlayersStats.most_red_carded;
            $scope.mostSubstituteOff = $scope.topPlayersStats.most_substitute_off;
            $scope.mostSubstituteIn = $scope.topPlayersStats.most_substitute_in;
            $scope.mostLineup = $scope.topPlayersStats.most_lineup;
            $scope.mostCaptain = $scope.topPlayersStats.most_captain;
            $scope.mostPenaltyMissed = $scope.topPlayersStats.most_penalty_missed;
            $scope.mostPlayed = $scope.topPlayersStats.most_played;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getCoachesStats = function () {
        $http({
            method: 'GET',
            url: '/api/top_coaches_stats'
        }).then(function successCallback(response) {
            $scope.topCoachesStats = response.data;

            $scope.mostTrainedCoach = $scope.topCoachesStats.most_trained;
            $scope.mostWinnerCoach = $scope.topCoachesStats.most_winner;
            $scope.mostLoserCoach = $scope.topCoachesStats.most_loser;
            $scope.mostWinnerCoachByPercentage = $scope.topCoachesStats.most_winner_by_percentage;
            $scope.mostLoserCoachByPercentage = $scope.topCoachesStats.most_loser_by_percentage;

            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getLongestStreaks = function () {
        $http({
            method: 'GET',
            url: '/api/longest_streaks'
        }).then(function successCallback(response) {
            $scope.longestStreaks = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getAverages = function () {
        $http({
            method: 'GET',
            url: '/api/averages'
        }).then(function successCallback(response) {
            $scope.averages = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getResultsSummary = function () {
        $http({
            method: 'GET',
            url: '/api/results_summary'
        }).then(function successCallback(response) {
            $scope.resultsSummary = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.gameSort = function(keyName){
        $scope.gameSortKey = keyName;   // Set the sortKey to the param passed.
        $scope.gameReverse = !$scope.gameReverse; // Perform negate on GameReverse (true->false, false->true).
    };

    $scope.ReportGame = function() {

        data = {
            game : $scope.GameToReport,
            message : $scope.ReportMessage
        };

        $http({
            method: 'POST',
            data: data,
            url: '/api/request'
        }).then(function successCallback(response) {
            $scope.CancelReport();
        }, function errorCallback(response) {
            $scope.ReportMessage = "אירעה שגיאה , אנא נסה שוב";
        })};

    $scope.SaveReportedGame = function(game) {
        $scope.GameToReport = game;
        $scope.WantToReport = true;
        $scope.ReportMessage = "ספר מה הדיבור";
    };

    $scope.CancelReport = function() {
        $scope.WantToReport = false;
        $scope.GameToReport = undefined;
        $scope.ReportMessage = "ספר מה הדיבור";
    };

    angular.element(document).ready(function () {
        $scope.getAvailableGameFilterOptions();
    });
});
