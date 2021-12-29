<template>
  <div class="timeline-wrapper">
    <Timeline :events="events" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      events: [
        {
          title: 'Schwanger',
          date: '2020-11-09',
          icon: '🤰🏼',
        },
        {
          title: 'Anfrage Gotti',
          date: '2020-12-29',
          icon: '👩‍👧',
        },
        {
          title: 'Häkelbuch',
          date: '2021-03-07',
          icon: '📓',
        },
        {
          title: 'Brunch auf Pläfe',
          date: '2021-04-18',
          icon: '🥐',
        },
        {
          title: 'Geburt',
          date: '2021-04-29',
          icon: '🐣',
        },
        {
          title: 'Erstes Video',
          date: '2021-05-02',
          icon: '🎥',
        },
        {
          title: 'Stofftier fertig',
          date: '2021-05-07',
          icon: '🦙',
        },
        {
          title: 'Erster Besuch Gotti',
          date: '2021-05-08',
          icon: '🙋‍♀️',
        },
        {
          title: 'Besuch Gotti',
          date: '2021-05-24',
          icon: '🙋‍♀️',
        },
        {
          title: 'Besuch Gotti',
          date: '2021-06-27',
          icon: '🙋‍♀️',
        },
        {
          title: 'Postkarte Gotti',
          date: '2021-07-13',
          icon: '💌',
        },
        {
          title: 'Ferienfotos',
          date: '2021-08-08',
          icon: '📸',
        },
        {
          title: 'Besuch Gotti',
          date: '2021-09-03',
          icon: '🙋‍♀️',
        },
        {
          title: 'Griechisches Essen',
          date: '2021-12-12',
          icon: '🇬🇷',
        },
      ],
    }
  },
}
</script>
<style>
.timeline-wrapper {
  height: 100vh;
}
</style>
