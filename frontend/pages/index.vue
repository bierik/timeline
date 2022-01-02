<template>
  <Timeline :events="events" class="timeline" />
</template>

<script>
export default {
  data() {
    return {
      events: [
        {
          title: 'Schwanger',
          start: '2020-11-09',
          icon: '🤰🏼',
        },
        {
          title: 'Anfrage Gotti',
          start: '2020-12-29',
          icon: '👩‍👧',
        },
        {
          title: 'Häkelbuch',
          start: '2021-03-07',
          icon: '📓',
        },
        {
          title: 'Brunch auf Pläfe',
          start: '2021-04-18',
          icon: '🥐',
        },
        {
          title: 'Geburt',
          start: '2021-04-29',
          icon: '🐣',
        },
        {
          title: 'Erstes Video',
          start: '2021-05-02',
          icon: '🎥',
        },
        {
          title: 'Stofftier fertig',
          start: '2021-05-07',
          icon: '🦙',
        },
        {
          title: 'Erster Besuch Gotti',
          start: '2021-05-08',
          icon: '🙋‍♀️',
        },
        {
          title: 'Besuch Gotti',
          start: '2021-05-24',
          icon: '🙋‍♀️',
        },
        {
          title: 'Besuch Gotti',
          start: '2021-06-27',
          icon: '🙋‍♀️',
        },
        {
          title: 'Postkarte Gotti',
          start: '2021-07-13',
          icon: '💌',
        },
        {
          title: 'Ferienfotos',
          start: '2021-08-08',
          icon: '📸',
        },
        {
          title: 'Besuch Gotti',
          start: '2021-09-03',
          icon: '🙋‍♀️',
        },
        {
          title: 'Griechisches Essen',
          start: '2021-12-12',
          icon: '🇬🇷',
        },
      ],
    }
  },
}
</script>
<style>
.timeline {
  height: 50vh;
}
</style>
