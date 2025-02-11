
<template>
    <vue-markdown :source="text" :options="md_options"/>
</template>


<script>

    import VueMarkdown from 'vue-markdown-render'

    export default {
        components: {
            VueMarkdown
        },
        props: {
            text: {required: true, type: String},
        },
        data () {
            var defaults = {
                    html: true,
                    typographer: true,
                    _highlight: true, // <= THIS IS WHAT YOU NEED
                };

                return {
                    md_options: defaults,
                }
        },
        methods: {

        }
    }
</script>
