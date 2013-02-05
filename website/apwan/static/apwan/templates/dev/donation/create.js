/**
 * Created with PyCharm.
 * User: Dean Gardiner
 * Date: 19/01/13
 * Time: 18:10
 * To change this template use File | Settings | File Templates.
 */

function get_val(element)
{
    var val = null;
    if(element.val() != '') {
        val = element.val();
    }
    return val;
}

$('#checkout_submit').click(do_donation);

var checkout_result = $('#checkout_result');

var result_template = Mustache.template('dev/donation/create_result');

function do_donation()
{
    var _recipient_id = parseInt(get_val($('#donation_recipient_id')));
    var _entity_id = parseInt(get_val($('#donation_entity_id')));
    var _amount = get_val($('#donation_amount'));

    checkout_result.text('');

    Dajaxice.donation.create(function(result) {
        process_result(result);
    }, {
        'recipient_id': _recipient_id,
        'entity_id': _entity_id,
        'amount': _amount
    });
}

function process_result(result)
{
    checkout_result.html(result_template.render(result));
}