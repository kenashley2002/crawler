def get_add_cart_nutrilite(userId, blockId):
  displayURL = 'http://crawler-robibot.herokuapp.com'
  json_result = {
    'messages':[
      {
        'attachment': {
          'type': 'template',
          'payload': {
            'template_type': 'generic',
            'image_aspect_ratio': 'square',
            'elements': [{
              'title': 'Welcome ' + str(userId),
              'subtitle': 'Choose your preferences',
              'buttons':[
                {
                  'type': 'web_url',
                  'url': displayURL + '/webview/webview-nutrilite?userId={userId}&blockId={blockId}'.format(userId = userId, blockId = blockId),
                  'title': 'Webview',
                  'messenger_extensions': True,
                  'webview_height_ratio': 'tall' # Med view
                }
              ]
            }]
          }
        }
      }
  ]}
  return json_result
