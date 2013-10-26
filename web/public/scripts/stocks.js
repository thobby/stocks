
var app = angular.module("stocksApp", ["ngGrid"]);

function dayTopStocksCtrl($scope, $http) {
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

function linearRegressionCtrl($scope, $http) {
  $http({method: "GET", url: "/linearRegression"})
    .success(function(data, status, headers, config) {
      $scope.linearRegression = data;
  })
    .error(function(data, status, headers, config) {
      console.log("Error getting linear regression on stocks");
  });

  $scope.gridOptions = {
    data: 'linearRegression',
    showFilter: true,
    columnDefs: [{ field: "name", width: 120, displayName: "Name"},
                { field: "gradient", width: 120, displayName: "Gradient"},
                { field: "intercept", width: 120, displayName: "Intercept"},
                { field: "r_value", width: 120, displayName: "r_value"},
                { field: "p_value", width: 120, displayName: "p_value"},
                { field: "std_err", width: 120, displayName: "std_err"}]
  };
  $scope.linearRegression = [];
}
