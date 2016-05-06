#!/usr/bin/env python

import sys
import StringIO
import tempfile
import os
import pdb

import Image
import ImageDraw
import cairo
import rsvg
import argparse
from images import *

def open_svgstring_as_image(string, width, height):
    try:
        tmpfd, tmppath = tempfile.mkstemp(".svg")
        tmpfile = os.fdopen(tmpfd, 'w')
        tmpfile.write(string)
        tmpfile.close()
        return open_svg_as_image(tmppath, width, height)
    finally:
        os.remove(tmppath)

def open_svg_as_image(fn, width, height):
    for i in range(10):
        try:
            tmpfd, tmppath = tempfile.mkstemp(".png")
            tmpfile = os.fdopen(tmpfd,'w')
            
            file = StringIO.StringIO()
            svgsurface = cairo.SVGSurface (file, width, height)
            svgctx = cairo.Context(svgsurface)
            svg = rsvg.Handle(file=fn)
            svgwidth = svg.get_property('width')
            svgheight = svg.get_property('height')
            svgctx.scale(width/float(svgwidth),height/float(svgheight))
            svg.render_cairo(svgctx)
            
            svgsurface.write_to_png(tmpfile)
            svgsurface.finish()
            tmpfile.close()
            
            tmpfile = open(tmppath, 'r')
            imgsurface = cairo.ImageSurface.create_from_png(tmpfile)
            imgwidth = imgsurface.get_width()
            imgheight = imgsurface.get_height()
            
            data = imgsurface.get_data()
        
            im = Image.frombuffer("RGBA",(imgwidth, imgheight), data ,"raw","RGBA",0,1)
            os.remove(tmppath)
            break
        except MemoryError:
            print 'Memory Error. Try again ...'
            continue
    else:
        raise Exception('Problem loading image {0}'.format(fn))
    return im   

def draw_board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
               title1="", title2="", footnote="", scale=1, flip = False):
    red = (255,0,0, 255)
    white_square = (255,255,255,255)
    black_square = (128,128,128,255)
    border_color = (156,156,156,255)
    font_color = (0,0,0,255)
    
    sqsize = 45
    border_width = 12
    bord_offset = 0
    title_height = 40
    sqoffset = border_width + bord_offset
    footnote_height = 20
    
    imgwidth = bord_offset + border_width * 2 + sqsize * 8
    imgheight = bord_offset + border_width * 2 + sqsize * 8 + title_height + footnote_height
    
    im = Image.new('RGBA', (imgwidth, imgheight))
    draw = ImageDraw.Draw(im)
    
    color = white_square

    # Draw Title

    t1_w,t1_h = draw.textsize(title1)
    t2_w,t2_h = draw.textsize(title2)
    freespace = title_height - (t1_h + t2_h)
    
    t1pos = (bord_offset + ((8*sqsize + 2*border_width)-t1_w)/2,
             bord_offset + freespace/3.0
             )
    draw.text(t1pos, title1, fill=font_color)
    t2pos = (bord_offset + ((8*sqsize + 2*border_width)-t2_w)/2,
             bord_offset + 2*freespace/3.0 + t1_h
             )
    draw.text(t2pos, title2, fill=font_color)
    
    # Draw footnote
    f_w,f_h = draw.textsize(footnote)
    fpos = (bord_offset + ((8*sqsize + 2*border_width)-f_w)/2,
            bord_offset +border_width * 2 + sqsize * 8 + title_height + (footnote_height - f_h)/2)
    draw.text(fpos, footnote, fill=font_color)
    
    # Draw Borders
    
    for i in range(8):
        colchr = chr(ord('8')-i)
        rowchr = chr(ord('a')+i)
        if(flip):
            colchr = chr(ord('1')+i)
            rowchr = chr(ord('h')-i)

        # Left border
        rect = (bord_offset,
                title_height + bord_offset+border_width+i*sqsize,
                bord_offset+border_width,
                title_height + bord_offset+border_width+(i+1)*sqsize
                )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        
        (w,h) = draw.textsize(colchr)
        textpos = (bord_offset + (border_width-w)/2,
                   title_height + bord_offset + (sqsize-h)/2 + border_width + i*sqsize)
        draw.text(textpos, colchr, fill=font_color)
        
        # Right Border
        rect = (8*sqsize + border_width + bord_offset,
                title_height + bord_offset + border_width + i*sqsize,
                8*sqsize + border_width + bord_offset + border_width,
                title_height + bord_offset + border_width + (i+1)*sqsize
                )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        
        (w,h) = draw.textsize(colchr)
        textpos = (8*sqsize + border_width + bord_offset + (border_width-w)/2,
                   title_height + bord_offset + (sqsize-h)/2 + border_width + i*sqsize)
        draw.text(textpos, colchr, fill=font_color)
        
        # Top Border
    
        rect = (bord_offset + border_width+i*sqsize,
                title_height + bord_offset,
                bord_offset + border_width+(i+1)*sqsize,
                title_height + bord_offset+border_width,
                )
        draw.rectangle(rect, fill=border_color, outline=border_color)
    
        (w,h) = draw.textsize(rowchr)
        textpos = (bord_offset + border_width + i*sqsize + (sqsize-w)/2,
                   title_height + bord_offset + (border_width-h)/2)
        draw.text(textpos, rowchr, fill=font_color)
        
        # Bottom Border
        
        rect = (
            bord_offset + border_width + i*sqsize,
            title_height + 8*sqsize + border_width + bord_offset,
            bord_offset + border_width + (i+1)*sqsize,
            title_height + 8*sqsize + border_width + bord_offset + border_width,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
    
        (w,h) = draw.textsize(rowchr)
        textpos = (bord_offset + border_width + i*sqsize + (sqsize-w)/2,
                   title_height + 8*sqsize + border_width + bord_offset + (border_width-h)/2)
        draw.text(textpos, rowchr, fill=font_color)
    
    # Draw the corners
        rect = (
            bord_offset,
            title_height + bord_offset,
            bord_offset + border_width,
            title_height + bord_offset + border_width,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        rect = (
            bord_offset + border_width + 8*sqsize,
            title_height + bord_offset,
            bord_offset + 2 * border_width + 8*sqsize,
            title_height + bord_offset + border_width,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        rect = (
            bord_offset + border_width + 8*sqsize,
            title_height + bord_offset + border_width + 8*sqsize,
            bord_offset + 2 * border_width + 8*sqsize,
            title_height + bord_offset + 2 * border_width + 8*sqsize,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        rect = (
            bord_offset,
            title_height + bord_offset + border_width + 8*sqsize,
            bord_offset + border_width,
            title_height + bord_offset + 2 * border_width + 8*sqsize,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
    
    # Draw the squares
    for row in range(8):
        for col in range(8):
            rect = (col*sqsize+sqoffset,
                    title_height + row*sqsize+sqoffset,
                    (col+1)*sqsize+sqoffset,
                    title_height + (row+1)*sqsize+sqoffset)
            draw.rectangle(rect, fill=color, outline=color)
            if color == black_square:
                color = white_square
            else:
                color = black_square
        if color == black_square:
            color = white_square
        else:
            color = black_square
    
    # Draw the pieces
    
    row, col = 8,1
    for c in fen:
        imgpos = (border_width+sqsize*(col-1),
                  title_height + border_width+sqsize*(8-row))
        if(flip):
            imgpos = (border_width+sqsize*(8-col),
                      title_height + border_width+sqsize*(row-1))
        if c == 'K':
            wking = open_svgstring_as_image(white_king, sqsize, sqsize)
            im.paste(wking, imgpos, wking)
            col += 1
        elif c == 'Q':
            wqueen = open_svgstring_as_image(white_queen, sqsize, sqsize)
            im.paste(wqueen, imgpos, wqueen)
            col += 1
        elif c == 'P':
            wpawn = open_svgstring_as_image(white_pawn, sqsize, sqsize)
            im.paste(wpawn, imgpos, wpawn)
            col += 1
        elif c == 'R':
            wrook = open_svgstring_as_image(white_rook, sqsize, sqsize)
            im.paste(wrook, imgpos, wrook)
            col += 1    
        elif c == 'B':
            wbishop = open_svgstring_as_image(white_bishop, sqsize, sqsize)
            im.paste(wbishop, imgpos, wbishop)
            col += 1
        elif c == 'N':
            wknight = open_svgstring_as_image(white_knight, sqsize, sqsize)
            im.paste(wknight, imgpos, wknight)
            col += 1
        elif c == 'k':
            wking = open_svgstring_as_image(black_king, sqsize, sqsize)
            im.paste(wking, imgpos, wking)
            col += 1
        elif c == 'q':
            wqueen = open_svgstring_as_image(black_queen, sqsize, sqsize)
            im.paste(wqueen, imgpos, wqueen)
            col += 1
        elif c == 'p':
            bpawn = open_svgstring_as_image(black_pawn, sqsize, sqsize)
            im.paste(bpawn, imgpos, bpawn)
            col += 1
        elif c == 'r':
            brook = open_svgstring_as_image(black_rook, sqsize, sqsize)
            im.paste(brook, imgpos, brook)
            col += 1
        elif c == 'b':
            bbishop = open_svgstring_as_image(black_bishop, sqsize, sqsize)
            im.paste(bbishop, imgpos, bbishop)
            col += 1
        elif c == 'n':
            bknight = open_svgstring_as_image(black_knight, sqsize, sqsize)
            im.paste(bknight, imgpos, bknight)
            col += 1  
        elif c in '12345678':
            col += int(c)
        elif c == '/':
            col = 1
            row -= 1
    return im.resize((int(scale*imgwidth),int(scale*imgheight)))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a chess board image from a fen description')
    parser.add_argument('fen', help='Position in the fen format')
    parser.add_argument('--title1', help='The first title', default='')
    parser.add_argument('--title2', help='The seconde title', default='')
    parser.add_argument('--footnote', help='Specify the footnote', default='')
    parser.add_argument('--size', help='Specify the size', default='')
    parser.add_argument('--scale', type=float, help='Specify a scale factor', default=1)
    parser.add_argument(
        '--outfile', type=argparse.FileType('w'), default=None,
        help='The png filename '
             '(default: write use the fen as filename)')

    args = parser.parse_args()
    if args.outfile == None:
        args.outfile = open(args.fen.replace('/','_') + '.png', 'w')
    
    if args.size != '':
        try:
            args.sizex, args.sizey = args.size.split('x')
            args.sizex = int(args.sizex)
            args.sizey = int(args.sizey)
        except ValueError:
            parser.print_usage()
            sys.exit(1)

    im = draw_board(args.fen, title1=args.title1,
                    title2=args.title2,
                    footnote=args.footnote,
                    scale=args.scale)
    if args.size != '':
        im = im.resize((args.sizex, args.sizey))
    im.save(args.outfile)
