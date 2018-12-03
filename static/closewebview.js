window.extAsyncInit = function() {
    console.log('Messenger extensions are ready');

    // Handle button click
    $('#preferencesForm').submit(function(event) {
      console.log('Submit pressed');

      event.preventDefault();

      const formData = $('#preferencesForm').serialize();

      $.post('broadcast-to-chatfuel', formData, function (data) {
                    MessengerExtensions.requestCloseBrowser(function success() {
                        // webview closed
                        console.log('Closed the window!');
                    }, function error(error) {
                        // an error occurred
                        console.log('Error closing browser window!');
                        console.log(error);
                        $('#infoMessage').text(`requestCloseBrowser error : ${error}`);
                    });
                });
    });

    }