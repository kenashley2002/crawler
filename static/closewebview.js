window.extAsyncInit = function() {
    console.log('Messenger extensions are ready');

    // Handle button click
    $('#preferencesForm').submit(function(event) {
      console.log('Submit pressed');

      event.preventDefault();

      const formData = $('#preferencesForm').serialize();

      $.post('broadcast-to-chatfuel', formData, function (data) {
        MessengerExtensions.requestCloseBrowser(function () {
          console.log('Window will be closed');
        }, function (error) {
          console.log('There is an error');
          console.log(error);
        });
      });
    });

    }