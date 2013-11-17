
var app = angular.module("stocksApp", ["ngGrid", "uiSlider"]);

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
      for (i = 0; i < data.length; i++) {
        if (data[i].gradient >= 0) {
          $scope.linearRegressionPlus += 1;
        } else {
          $scope.linearRegressionMinus += 1;
        }
      }
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
  $scope.linearRegressionPlus = 0;
  $scope.linearRegressionMinus = 0;

  $scope.$watch('minDatumTS', function(newValue, oldValue) {
    // newValue is in days therefore conversion to ms is needed
    // 01-01-2013 is 1356998400000 ms since 1970
    $scope.minDatum = 1356998400000 + 1000 * 3600 * 24 * (newValue - 1);
  });

  $scope.$watch('maxDatumTS', function(newValue, oldValue) {
    // newValue is in days therefore conversion to ms is needed
    // 01-01-2013 is 1356998400000 ms since 1970
    $scope.maxDatum = 1356998400000 + 1000 * 3600 * 24 * (newValue - 1);
  });

  $scope.minDatumTS = 1;
  $scope.maxDatumTS = 365;

}
