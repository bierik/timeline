<template>
  <form @submit.prevent="_save" @reset.prevent="cancel">
    <slot />
    <div class="flex">
      <div class="grow" />
      <Button type="submit" :loading="loading">Speichern</Button>
      <ButtonSecondary type="reset">Abbrechen</ButtonSecondary>
    </div>
  </form>
</template>

<script>
import formMixin from '@/components/form/form-mixin'
export default {
  name: 'Form',
  mixins: [formMixin],
}
</script>
