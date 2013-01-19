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

$('#checkout_submit').click(do_checkout);

function do_checkout()
{
    var _recipient_id = parseInt(get_val($('#donation_recipient_id')));
    var _entity_id = parseInt(get_val($('#donation_entity_id')));
    var _amount = get_val($('#donation_amount'));

    Dajaxice.donation.checkout(function(result) {
        process_result(result);
    }, {
        'recipient_id': _recipient_id,
        'entity_id': _entity_id,
        'amount': _amount
    });
}

function process_result(result)
{
    console.log(result);
}