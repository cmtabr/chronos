// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: "Chronos",
			description:
				"Documentação do Chronos — API REST com FastAPI, SQLAlchemy e PostgreSQL.",
			social: [
				{
					icon: "github",
					label: "GitHub",
					href: "https://github.com/cmtabr/chronos",
				},
			],
			editLink: {
				baseUrl: "https://github.com/cmtabr/chronos/edit/main/docs/",
			},
			sidebar: [
				{
					label: "Documentação",
					items: [
						{ label: "Início", link: "/" },
						{ label: "Introdução", slug: "intro" },
					],
				},
			],
		}),
	],
});
