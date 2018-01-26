var app = angular.module('MaccabiStatsApp', []);
app.controller('MaccabiStatsController', function ($scope, $http) {
    $scope.got_opponents = false;
    $scope.got_competitions = false;
    $scope.All = "הכל";
    $scope.firstLeague = "ליגה ראשונה";
    $scope.LocationOptions = ["הכל", "בית", "חוץ"];
    $scope.SelectedLocation = $scope.All;
    $scope.OnlyWins = false;
    $scope.AfterDate = new Date("1900");
    $scope.BeforeDate = new Date();
    $scope.Competition = $scope.All;
    $scope.limit = 10;

    $scope.getstats = function () {

        // Remove current stats
        $scope.bestScorers = undefined;
        $scope.bestAssisters = undefined;
        $scope.mostYellowCarded = undefined;
        $scope.mostLineupPlayers = undefined;
        $scope.mostTrainedCoach = undefined;
        $scope.mostWinnerCoach = undefined;
        $scope.mostLoserCoach = undefined;
        $scope.mostWinnerCoachByPercentage = undefined;
        $scope.mostLoserCoachByPercentage = undefined;
        $scope.longestWinsStreakGames = undefined;
        $scope.longestUnbeatenStreakGames= undefined;
        $scope.longestScoredStreakGames = undefined;
        $scope.longestCleanSheetStreakGames = undefined;


        data = {
            opponent: $scope.SelectedOpponent.trim(),
            location: $scope.SelectedLocation.trim(),
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
            $scope.getBestScorers();
            $scope.getBestAssisters();
            $scope.getMostYellowCarded();
            $scope.getMostLineupPlayers();
            $scope.getMostTrainedCoach();
            $scope.getMostWinnerCoach();
            $scope.getMostLoserCoach();
            $scope.getMostWinnerCoachByPercentage();
            $scope.getMostLoserCoachByPercentage();
            $scope.getLongestWinsStreakGames();
            $scope.getLongestUnbeatenStreakGames();
            $scope.getLongestScoredStreakGames();
            $scope.getLongestCleanSheetStreakGames();

        }, function errorCallback(response) {
            $scope.msg = "server error";
        });
    };

    $scope.getAvailableOpponents = function () {
        $http({
            method: 'GET',
            url: '/api/opponents'
        }).then(function successCallback(response) {
            $scope.SelectedOpponent = $scope.All;
            $scope.AvailableOpponents = response.data;
            $scope.AvailableOpponents.push($scope.All);    
            $scope.got_opponents = true;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getAvailableCompetitions = function () {
        $http({
            method: 'GET',
            url: '/api/competitions'
        }).then(function successCallback(response) {
            $scope.SelectedCompetition = $scope.All;
            $scope.AvailableCompetitions = response.data;
            $scope.AvailableCompetitions.push($scope.All);
            $scope.AvailableCompetitions.push($scope.firstLeague);
            $scope.got_competitions = true;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getBestScorers = function () {
        $http({
            method: 'GET',
            url: '/api/best_scorers'
        }).then(function successCallback(response) {
            $scope.bestScorers = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getBestAssisters = function () {
        $http({
            method: 'GET',
            url: '/api/best_assisters'
        }).then(function successCallback(response) {
            $scope.bestAssisters = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getMostYellowCarded = function () {
        $http({
            method: 'GET',
            url: '/api/most_yellow_carded'
        }).then(function successCallback(response) {
            $scope.mostYellowCarded = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getMostLineupPlayers = function () {
        $http({
            method: 'GET',
            url: '/api/most_lineup_players'
        }).then(function successCallback(response) {
            $scope.mostLineupPlayers = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };
    
    $scope.getMostTrainedCoach = function () {
        $http({
            method: 'GET',
            url: '/api/most_trained_coach'
        }).then(function successCallback(response) {
            $scope.mostTrainedCoach = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };
    
    $scope.getMostWinnerCoach = function () {
        $http({
            method: 'GET',
            url: '/api/most_winner_coach'
        }).then(function successCallback(response) {
            $scope.mostWinnerCoach = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };
    
    $scope.getMostLoserCoach = function () {
        $http({
            method: 'GET',
            url: '/api/most_loser_coach'
        }).then(function successCallback(response) {
            $scope.mostLoserCoach = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };
    
    $scope.getMostWinnerCoachByPercentage = function () {
        $http({
            method: 'GET',
            url: '/api/most_winner_coach_by_percentage'
        }).then(function successCallback(response) {
            $scope.mostWinnerCoachByPercentage = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };
    
    $scope.getMostLoserCoachByPercentage = function () {
        $http({
            method: 'GET',
            url: '/api/most_loser_coach_by_percentage'
        }).then(function successCallback(response) {
            $scope.mostLoserCoachByPercentage = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getLongestWinsStreakGames = function () {
        $http({
            method: 'GET',
            url: '/api/longest_wins_streak_games'
        }).then(function successCallback(response) {
            $scope.longestWinsStreakGames = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getLongestUnbeatenStreakGames = function () {
        $http({
            method: 'GET',
            url: '/api/longest_unbeaten_streak_games'
        }).then(function successCallback(response) {
            $scope.longestUnbeatenStreakGames = response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getLongestScoredStreakGames = function () {
        $http({
            method: 'GET',
            url: '/api/longest_score_streak_games'
        }).then(function successCallback(response) {
            $scope.longestScoredStreakGames= response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };

    $scope.getLongestCleanSheetStreakGames = function () {
        $http({
            method: 'GET',
            url: '/api/longest_clean_sheet_streak_games'
        }).then(function successCallback(response) {
            $scope.longestCleanSheetStreakGames= response.data;
            console.log(response.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };



    angular.element(document).ready(function () {
        $scope.getAvailableOpponents();
        $scope.getAvailableCompetitions();
    });
});
