<template>
  <form @submit.prevent="_save" @reset.prevent="cancel">
    <slot />
    <div class="flex pt-4">
      <Button type="submit" :loading="loading" class="mr-2">Speichern</Button>
      <ButtonSecondary type="reset">Abbrechen</ButtonSecondary>
      <div class="grow" />
      <slot name="action-before" />
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
