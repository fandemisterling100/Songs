import { extend } from 'vee-validate'
import required, * as rules from 'vee-validate/dist/rules';

Object.keys(rules).forEach(rule => {
  extend(rule, rules[rule]);
});

extend('required', {
  ...required,
  message: (fieldName) => {
    return `${fieldName} es un campo obligatorio`;
  }
});

extend('checked', {
  validate: value => value.length > 0,
  message: "Debese seleccionar al menos una opción"
})
