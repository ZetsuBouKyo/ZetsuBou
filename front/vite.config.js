import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Components from "unplugin-vue-components/vite";
import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";
import path from "path";

export default defineConfig({
    plugins: [
        vue(),
        Components({
            dirs: [],
            resolvers: [
                // auto import icons
                // https://github.com/antfu/unplugin-icons
                IconsResolver({
                    componentPrefix: "icon",
                }),
            ],
        }),
        Icons(),
    ],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "/src"),
        },
    },
    server: {
        open: true,
    },
    build: {
        sourcemap: true,
    },
});
