import os

CACHE_DIR = './cache'
TRANSCRIPTS_DIR = CACHE_DIR + '/video_transcripts'

if __name__ == '__main__':
	filenames = os.listdir(TRANSCRIPTS_DIR)
	with open(CACHE_DIR + '/yt_transcript_index.csv', 'w') as outfile:
		for fname in filenames:
			with open(TRANSCRIPTS_DIR + '/' + fname) as infile:
				for line in infile:
					split_line = line.strip().split(';')

					video_id = fname.replace('.csv', '')
					start = split_line.pop(0)
					vtext = ''.join(split_line)

					line_text = "{},{},\"{}\"".format(video_id, start, vtext)
					print(line_text)
					outfile.write(line_text + '\n')