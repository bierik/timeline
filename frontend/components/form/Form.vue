<template>
  <form class="pb-20" @submit.prevent="_save" @reset.prevent="cancel">
    <slot />
    <div class="fixed bottom-0 left-0 right-0 bg-primary-50">
      <div class="container flex p-4">
        <slot name="action-before" />
        <ButtonDelete v-if="!disableRemove" @click="_remove" />
        <div class="grow" />
        <ButtonSecondary class="mr-2" type="reset">
          <feather class="inline-block md:!hidden" size="20" type="x" />
          <span class="hidden md:block">Abbrechen</span>
        </ButtonSecondary>
        <Button type="submit" :loading="loading">
          <feather class="inline-block md:!hidden" size="20" type="check" />
          <span class="hidden md:block">Speichern</span>
        </Button>
      </div>
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
