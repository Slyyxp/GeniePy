#!/usr/bin/env python3
import argparse
import os
import sys
from urllib import parse
import mutagen.id3 as id3
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError
from tqdm import tqdm
from requests import HTTPError

from modules import client, config, exceptions, logger, utils


def getargs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', nargs="*", help="URL.", required=True)
	parser.add_argument('-f', help="Format. 1: MP3, 2: 16-bit FLAC, 3: 24-bit FLAC",
	                    default=prefs['default_format'], choices=[1, 2, 3], type=int
	                    )
	return parser.parse_args()


def download_track(url, title, abs, cur, total, specs):
	"""
	:param url: Direct stream link to the track
	:param title: Title of the song for tqdm progress
	:param abs: Path of the file we'll download it to.
	:param cur: Track number
	:param total: Track total
	:param specs: Track specifications
	"""
	print('\nDownloading track {} of {}: {} - {}'.format(cur, total, title, specs))
	r = client.session.get(parse.unquote(url), stream=True)
	r.raise_for_status()
	size = int(r.headers.get('content-length', 0))
	with open(abs, 'wb') as f:
		with tqdm(total=size, unit='B',
		          unit_scale=True, unit_divisor=1024,
		          initial=0, miniters=1) as bar:
			for chunk in r.iter_content(32 * 1024):
				if chunk:
					f.write(chunk)
					bar.update(len(chunk))

def download_cover(cover_url, path):
	"""
	:param cover_url: Direct url to the cover artwork
	:param path: Path to download the cover to
	"""
	path = os.path.join(path, prefs['cover_name'])
	if not utils.exist_check(path):
		r = client.session.get(cover_url)
		with open(path, 'wb') as f:
			f.write(r.content)

def fix_tags(abs, ext, f_meta):
	"""
	:param abs: Path of the file we're tagging
	:param ext: Extension of the file we're tagging
	:param f_meta: Dict containing the metadata of the track we're tagging.
	"""
	if ext == "mp3":
		try:
			audio = id3.ID3(abs)
		except ID3NoHeaderError:
			audio = id3.ID3()
		audio['TRCK'] = id3.TRCK(text=str(audio['TRCK']) + "/" + str(f_meta['track_total']))
		audio['TPOS'] = id3.TPOS(text=str(audio['TPOS']) + "/" + str(f_meta['disc_total']))
		audio['TDRC'] = id3.TPOS(text=f_meta['release_date'])
		audio['TPUB'] = id3.TPOS(text=f_meta['planning'])
		audio['TPE1'] = id3.TPE1(text=f_meta['track_artist'])
		audio['TPE2'] = id3.TPE2(text=f_meta['album_artist'])
		audio.save(abs, "v2_version=3")
	else:
		audio = FLAC(abs)
		audio['TRACKTOTAL'] = str(f_meta['track_total'])
		audio['DISCTOTAL'] = str(f_meta['disc_total'])
		audio['DATE'] = f_meta['release_date']
		audio['LABEL'] = f_meta['planning']
		audio['ARTIST'] = f_meta['track_artist']
		audio['ALBUMARTIST'] = f_meta['album_artist']
		audio.save()


def main():
	"""
	Main function which will control the flow of our script when called.
	"""
	total = len(args.u)
	for n, url in enumerate(args.u, 1):
		logger_genie.info("Album {} of {}".format(n, total))
		album_id = utils.check_url(url)
		if not album_id:
			return
		meta = client.get_meta(album_id)
		album_fol = "{} - {}".format(
			parse.unquote(meta['DATA0']['DATA'][0]['ARTIST_NAME']),
			parse.unquote(meta['DATA0']['DATA'][0]['ALBUM_NAME'])
		)
		if prefs['artist_folders']:
			album_fol_abs = os.path.join(
				os.path.dirname(__file__), prefs['download_directory'],
				parse.unquote(utils.sanitize(meta['DATA0']['DATA'][0]['ARTIST_NAME'])), utils.sanitize(album_fol)
			)
		else:
			album_fol_abs = os.path.join(
				os.path.dirname(__file__), prefs['download_directory'], utils.sanitize(album_fol)
			)
		logger_genie.info("Album found: " + album_fol)
		utils.make_dir(album_fol_abs)
		cover_url = parse.unquote(meta['DATA0']['DATA'][0]['ALBUM_IMG_PATH_600'])
		# If no 600x600 artwork is present then fallback to what's available
		if not cover_url:
			cover_url = parse.unquote(meta['DATA0']['DATA'][0]['ALBUM_IMG_PATH'])
		download_cover(cover_url, album_fol_abs)
		f_meta = {
			"track_total": len(meta['DATA1']['DATA']),
			"album_artist": parse.unquote(meta['DATA0']['DATA'][0]['ARTIST_NAME']),
			"release_date": meta['DATA0']['DATA'][0]['ALBUM_RELEASE_DT'],
			"planning": parse.unquote(meta['DATA0']['DATA'][0]['ALBUM_PLANNER'])
		}
		f_meta['disc_total'] = meta['DATA1']['DATA'][f_meta['track_total'] - 1]['ALBUM_CD_NO']
		for track in meta['DATA1']['DATA']:
			try:
				s_meta = client.get_stream_meta(track['SONG_ID'], args.f)
			except HTTPError:
				logger_genie.warning("Could not get stream info for {}".format(track['SONG_ID']))
				continue
			except exceptions.StreamMetadataError:
				continue
			cur = track['ROWNUM']
			track_title = parse.unquote(track['SONG_NAME'])
			f_meta['track_artist'] = parse.unquote(track['ARTIST_NAME'])
			ext = utils.get_ext(s_meta['FILE_EXT'])
			post_abs = os.path.join(
				album_fol_abs, "{}. {}.{}".format(
					cur.zfill(2), utils.sanitize(track_title), ext
				)
			)
			if utils.exist_check(post_abs):
				continue
			if not utils.allowed_check(s_meta['STREAMING_LICENSE_YN']):
				continue
			pre_abs = os.path.join(album_fol_abs, cur + ".genie-dl")
			specs = utils.parse_specs(s_meta['FILE_EXT'], s_meta['FILE_BIT'])
			download_track(s_meta['STREAMING_MP3_URL'], track_title,
			               pre_abs, cur, f_meta['track_total'], specs
			               )
			try:
				fix_tags(pre_abs, ext, f_meta)
				logger_genie.debug("Tags updated: {}".format(f_meta))
			except Exception as e:
				raise e
			try:
				os.rename(pre_abs, post_abs)
				logger_genie.debug("{} has been renamed".format(post_abs))
			except OSError:
				raise exceptions.TrackRenameError("Could not rename {}".format(pre_abs))


if __name__ == '__main__':
	try:
		client = client.Client()
		prefs = config.prefs
		if prefs['ascii_art']:
			utils.print_title()
		args = getargs()
		logger_genie = logger.log_setup()
		logger_genie.debug(args)
		args.f = {1: 320, 2: 1000, 3: "24bit"}[args.f]
		client.auth()
		main()
	except KeyboardInterrupt:
		sys.exit()
