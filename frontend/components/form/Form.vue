<template>
  <form class="pb-20" @submit.prevent="_save" @reset.prevent="cancel">
    <slot />
    <div class="fixed inset-x-0 bottom-0 bg-primary-50">
      <div class="container flex p-4">
        <slot name="action-before" />
        <ButtonDelete v-if="!disableRemove" @click="_remove" />
        <div class="grow" />
        <ButtonSecondary class="mr-2" type="reset">
          <Icon class="inline-block md:!hidden" size="20" name="feather:x" />
          <span class="hidden md:block">Abbrechen</span>
        </ButtonSecondary>
        <Button type="submit" :loading="loading">
          <Icon
            class="inline-block md:!hidden"
            size="20"
            name="feather:check"
          />
          <span class="hidden md:block">Speichern</span>
        </Button>
      </div>
    </div>
  </form>
</template>

<script>
import formMixin from "@/components/form/form-mixin";
export default defineNuxtComponent({
  name: "SubmitForm",
  mixins: [formMixin],
});
</script>
