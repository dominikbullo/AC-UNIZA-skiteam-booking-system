// RES: https://stackoverflow.com/questions/53436941/django-admin-on-form-change
django.jQuery(document).ready(function () {
  console.log('ready!')
  django.jQuery('#id_name').change(function () {
    alert('Handler for #id_name was called.')
    // TODO base on category name
    django.jQuery('#id_year_from')[0].value = new Date().getFullYear() - 20
    django.jQuery('#id_year_until')[0].value = new Date().getFullYear() - 18
    // RES: https://stackoverflow.com/questions/15066971/django-admin-populate-the-field-based-on-previous-field-value
  })
  // django.jQuery('#id_year_from').change(function () {
  //   alert('Handler for #id_year_from was called.')
  // })
  // django.jQuery('#id_year_until').change(function () {
  //   alert('Handler for #id_year_until was called.')
  // })
})
