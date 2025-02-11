
<template>
    <vue-markdown :source="md_text" :options="md_options"/>
</template>


<script>

    import VueMarkdown from 'vue-markdown-render'

    export default {
        components: {
            VueMarkdown
        },
        props: {
        },
        data () {
            var defaults = {
                    html: true,
                    typographer: true,
                    _highlight: true, // <= THIS IS WHAT YOU NEED
                };

                return {
                    md_options: defaults,
                    md_text: "# Hello World!",
                }
        },
        methods: {

        }
    }
</script>
