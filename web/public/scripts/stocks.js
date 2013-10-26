
var app = angular.module("stocksApp", ["ngGrid"]);

function MyCtrl($scope, $http) {
  $http({method: "GET", url: "/dayTopStocks"})
    .success(function(data, status, headers, config) {
      $scope.dayTopStocks = data;
  })
    .error(function(data, status, headers, config) {
      console.log("Error getting day top stocks");
  });

  $scope.gridOptions = {
    data: 'dayTopStocks',
    showFilter: true,
    columnDefs: [{ field: "name", width: 120, displayName: "Name"},
                { field: "datum", width: 120, displayName: "Datum"},
                { field: "gain", width: 120, displayName: "Gain"}]
  };
  $scope.dayTopStocks = [];
}

