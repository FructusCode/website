/**
 * Created with PyCharm.
 * User: Dean Gardiner
 * Date: 19/01/13
 * Time: 17:36
 * To change this template use File | Settings | File Templates.
 */
var example_data = {
    0: ['Chuck', 'Eureka', 'Fringe'],
    1: [{
        title: 'The Hitchhiker\'s Guide to the Galaxy',
        year: 2005
    },
        {
            title: 'Skyfall',
            year: 2012
        },
        {
            title: 'Taken',
            year: 2008
        },
        {
            title: 'Taken 2',
            year: 2012
        }
    ],
    2: [
        {
            'artist': "M83"
        },
        {
            'artist': "M83",
            'track': "Intro"
        },
        {
            'artist': "Everything Everything",
            'album': "Arc"
        },
        {
            'artist': "Everything Everything",
            'track': "Weights"
        }
    ],
    3: []
};

var _search_type = $('#search_type');
var _search_title = $('#search_title');
var _search_year = $('#search_year');
var _search_artist = $('#search_artist');
var _search_album = $('#search_album');
var _search_track = $('#search_track');
var _results = $('#results');

$('#search_submit').click(do_search);
_search_title.keydown(function(event) {
    if(event.keyCode == 13)
    {
        do_search();
    }
});

function get_val(element)
{
    var val = null;
    if(element.val() != '') {
        val = element.val();
    }
    return val;
}

function load_example_data()
{
    var type = parseInt(_search_type.val());
    var rand = Math.floor(Math.random() * example_data[type].length);

    if(type == 2) {
        _search_title.val('');
        _search_year.val('');
        _search_artist.val(example_data[type][rand]['artist']);
        _search_album.val(example_data[type][rand]['album']);
        _search_track.val(example_data[type][rand]['track']);
    } else if(type == 1) {
        _search_title.val(example_data[type][rand]['title']);
        _search_year.val(example_data[type][rand]['year']);
        _search_artist.val('');
        _search_album.val('');
        _search_track.val('');
    } else {
        _search_title.val(example_data[type][rand]);
        _search_year.val('');
        _search_artist.val('');
        _search_album.val('');
        _search_track.val('');
    }
}
load_example_data();

function process_result(result)
{
    console.log('success: ' + result.success);

    if(result.success)
    {
        for(var i = 0; i < result.items.length; i++)
        {
            console.log(result.items[i]);
            if(result.items[i].type == 2) // if MUSIC
            {
                _results.prepend("<div style=\"width: 300px; border: 1px solid black; margin: 3px; padding: 3px; text-align: left;\">" +
                    "<b>ID:</b> <span>" + result.items[i].id + "</span><br/>" +
                    "<br/>" +
                    "<b>Artist:</b> <span>\"" + result.items[i].artist + "\"</span><br/>" +
                    "<b>Album:</b> <span>\"" + result.items[i].album + "\"</span><br/>" +
                    "<b>Track:</b> <span>\"" + result.items[i].track + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Image:</b> <span>\"" + result.items[i].image + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Recipients[0] ID:</b> <span>" + result.items[i].recipients[0].id + "</span><br/>" +
                    "<b>Recipients[0] title:</b> <span>\"" + result.items[i].recipients[0].title + "\"</span><br/>" +
                    "<b>Recipients[0] type:</b> <span>" + result.items[i].recipients[0].type + "</span><br/>" +
                    "</div>");
            } else if(result.items[i].type == 1) {
                _results.prepend("<div style=\"width: 300px; border: 1px solid black; margin: 3px; padding: 3px; text-align: left;\">" +
                    "<b>ID:</b> <span>\"" + result.items[i].id + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Title:</b> <span>\"" + result.items[i].title + "\"</span><br/>" +
                    "<b>Year:</b> <span>\"" + result.items[i].year + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Image:</b> <span>\"" + result.items[i].image + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Recipients[0] ID:</b> <span>" + result.items[i].recipients[0].id + "</span><br/>" +
                    "<b>Recipients[0] title:</b> <span>\"" + result.items[i].recipients[0].title + "\"</span><br/>" +
                    "<b>Recipients[0] type:</b> <span>" + result.items[i].recipients[0].type + "</span><br/>" +
                    "</div>");
            } else {
                _results.prepend("<div style=\"width: 300px; border: 1px solid black; margin: 3px; padding: 3px; text-align: left;\">" +
                    "<b>ID:</b> <span>\"" + result.items[i].id + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Title:</b> <span>\"" + result.items[i].title + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Image:</b> <span>\"" + result.items[i].image + "\"</span><br/>" +
                    "<br/>" +
                    "<b>Recipients[0] ID:</b> <span>" + result.items[i].recipients[0].id + "</span><br/>" +
                    "<b>Recipients[0] title:</b> <span>\"" + result.items[i].recipients[0].title + "\"</span><br/>" +
                    "<b>Recipients[0] type:</b> <span>" + result.items[i].recipients[0].type + "</span><br/>" +
                    "</div>");
            }
        }
    } else {
        console.log(result.error);
    }
}

function do_search()
{
    var type = null;
    if(_search_type.val() != '') {
        type = parseInt(_search_type.val());
    }

    var params = {};

    if(type == 2)
    {
        var artist = get_val(_search_artist);
        var album = get_val(_search_album);
        var track = get_val(_search_track);

        console.log("Searching '" + artist + "','" + album + "','" + track + "', (" + type + ")");

        params = {'type':type, 'artist': artist};
        if(album != null) params['album'] = album;
        if(track != null) params['track'] = track;
    } else {
        var title = get_val(_search_title);

        params = {'type':type, 'title': title};

        if(type == 1) {
            var year = null;
            if(_search_year.val() != '') {
                year = parseInt(_search_year.val());
            }
            params['year'] = year;
        }
    }

    Dajaxice.entity.search(function(result) {
        process_result(result);
    }, params);
}