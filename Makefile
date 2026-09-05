SHELL := /bin/bash

# make token — bir gizli değeri ~/.zshenv'e ekler ya da günceller.
# Adı sorar, değeri gizli alır (ekranda görünmez), önce yedek alır,
# aynı ad varsa satırı değiştirir. Değer hiçbir zaman ekrana basılmaz.
# Not: make 3.81'de .ONESHELL yok — recipe tek mantıksal satır.
.PHONY: token
token:
	@read -p "Env adı (örn. MCP_BEARER_TOKEN): " ad; \
	if [ -z "$$ad" ]; then echo "ad boş olamaz"; exit 1; fi; \
	if ! [[ "$$ad" =~ ^[A-Za-z_][A-Za-z0-9_]*$$ ]]; then echo "geçersiz ad: $$ad"; exit 1; fi; \
	read -s -p "Değer (gizli): " deger; echo; \
	if [ -z "$$deger" ]; then echo "değer boş olamaz"; exit 1; fi; \
	touch ~/.zshenv; cp ~/.zshenv ~/.zshenv.yedek; \
	if grep -q "^export $$ad=" ~/.zshenv; then islem="güncellendi"; \
	  grep -v "^export $$ad=" ~/.zshenv > ~/.zshenv.tmp && mv ~/.zshenv.tmp ~/.zshenv; \
	else islem="eklendi"; fi; \
	printf "export %s='%s'\n" "$$ad" "$$deger" >> ~/.zshenv; \
	chmod 600 ~/.zshenv; \
	echo "$$islem: $$ad (yedek: ~/.zshenv.yedek — yeni terminalde ya da 'source ~/.zshenv' ile geçerli)"
