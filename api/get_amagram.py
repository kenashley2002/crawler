import requests


def get_amagram():
    amagram = {
        'title': ['Amagram Tháng 11/2018', 'Amagram Tháng 10/2018'],
        'url': [
            'http://www.amwaytoday.com.vn/content/dam/websites/asia-pac/southeast-asia/vietnam/AmwayToday/document/vn_Tap_chi_amagram_thang11.18_lr.pdf',
            'http://www.amwaytoday.com.vn/content/dam/websites/asia-pac/southeast-asia/vietnam/AmwayToday/document/vn_Tap_chi_amagram_thang10.18.pdf'
        ],
        'img': [
            'http://www.amwaytoday.com.vn/tai-lieu-ho-tro/amagram/amagram-thang-11-2018.img.png/1540804242278.jpg',
            'http://www.amwaytoday.com.vn/tai-lieu-ho-tro/amagram/amagram-thang-10-2018.img.png/1538119416526.jpg'
        ],
    }

    json_result = {
        'messages': [
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'image_aspect_ratio': 'square',
                        'elements': [
                            {
                                'title': amagram['title'][0],
                                'image_url': amagram['img'][0],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'title': 'Xem',
                                        'type': 'web_url',
                                        'url': amagram['url'][0]
                                    }
                                ]
                            },
                            {
                                'title': amagram['title'][1],
                                'image_url': amagram['img'][1],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'title': 'Xem',
                                        'type': 'web_url',
                                        'url': amagram['url'][1]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        ]
    }
    return  json_result

