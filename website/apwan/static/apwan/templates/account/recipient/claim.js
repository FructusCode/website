var search_results = $('#search_results');
var search_submit = $('#search_submit');
var search_title = $('#search_title');

var item_template = Mustache.template('account/recipient/claim_item');

search_submit.click(search);

$(document).ready(function() {
    if(search_title.val() != '') search();
});

function search()
{
    Dajaxice.recipient.search(search_callback, {
        'title': search_title.val(),
        'entities_include': true,
        'limit': 9
    });
}

function search_callback(result)
{
    if(result.success)
    {
        search_results.empty();
        if(result.items.length > 0)
        {
            for(var i = 0; i < result.items.length; i++)
            {
                var recipient = result.items[i];

                for(var j = 0; j < recipient.entities.length; j++)
                {
                    recipient.entities[j].is_music = recipient.entities[j].type == 2;
                }

                if('entities_more' in recipient)
                {
                    if(recipient.entities_more == 1)
                    {
                        recipient.entities_more_tag = "entity";
                    } else {
                        recipient.entities_more_tag = "entities";
                    }
                }

                search_results.append(item_template.render({'recipient': recipient}));
            }
        } else {
            // TODO: Allow a recipient lookup here
        }
    }
}

function claim(recipient_id)
{
    console.log("claim(" + recipient_id + ")");

    Dajaxice.recipient.claim(claim_callback, {
        'recipient_id': recipient_id
    });
}

function claim_callback(result)
{
    var claim_element = $('.claim_item[recipient_id="' + result.recipient_id + '"]');
    if(claim_element != null)
    {
        if(result.success)
        {
            console.log(result);
            $('.claim-actions', claim_element)
                .html('<a href="/account/recipient/' + result.recipient_id + '" class="btn btn-mini btn-success">View</a>');
        } else {
            $('.claim-error', claim_element)
                .text("Failed")
                .delay(5000)
                .animate({
                    opacity: 0
                }, 2500, function() {
                    $(this).text('');
                    $(this).css('opacity', 1);
                });
        }
    } else {
        console.error("Bad 'claim_callback' result");
    }
}