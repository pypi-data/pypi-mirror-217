# -*- coding: utf-8 -*-
# @Organization  : changanqiche
# @Author        : Tang zhaoxiang
# @Time          : 2023/1/12 15:28
# @Function      : 从YEDDA中提取
import re

def removeRecommendContent(content, recommendRe=r'\[\$.*?\#.*?\*\](?!\#)'):
    output_content = ""
    last_match_end = 0
    for match in re.finditer(recommendRe, content):
        matched = content[match.span()[0]:match.span()[1]]
        words = matched.strip('[$]').split("#")[0]
        output_content += content[last_match_end:match.span()[0]] + words
        last_match_end = match.span()[1]
    output_content += content[last_match_end:]
    return output_content


def outputWithTagScheme(input_list, label, tagScheme="BMES"):
    output_list = []
    list_length = len(input_list)
    if tagScheme == "BMES":
        if list_length == 1:
            pair = input_list[0] + ' ' + 'S-' + label + '\n'
            output_list.append(pair)
        else:
            for idx in range(list_length):
                if idx == 0:
                    pair = input_list[idx] + ' ' + 'B-' + label + '\n'
                elif idx == list_length - 1:
                    pair = input_list[idx] + ' ' + 'E-' + label + '\n'
                else:
                    pair = input_list[idx] + ' ' + 'M-' + label + '\n'
                output_list.append(pair)
    else:  # BIO
        for idx in range(list_length):
            if idx == 0:
                pair = input_list[idx] + ' ' + 'B-' + label + '\n'
            else:
                pair = input_list[idx] + ' ' + 'I-' + label + '\n'
            output_list.append(pair)
    return output_list

def turnFullListToOutputPair(fullList, segmented=True, tagScheme="BMES", onlyNP=False):
    pair_list = []
    for chunk_words, start, end, is_tagged in fullList:
        if is_tagged:
            plain_words, label = chunk_words.strip('[@$]').rsplit('#', 1)
            label = label.strip('*')
            if segmented:
                plain_words = plain_words.split()
            if onlyNP:
                label = "NP"
            outList = outputWithTagScheme(plain_words, label, tagScheme)
            pair_list.extend(outList)
        else:
            if segmented:
                words = chunk_words.split()
            else:
                words = chunk_words  # actually chars
            for word_or_char in words:
                if word_or_char == ' ':
                    continue
                pair = word_or_char + ' ' + 'O\n'
                pair_list.append(pair)
    return pair_list

def getWordTagPairs(tagedSentence, segmented=True, tagScheme="BMES", onlyNP=False, entityRe=r'\[\@.*?\#.*?\*\]'):
    sentence = tagedSentence.strip('\n')
    tagged_chunks = []
    for match in re.finditer(entityRe, sentence):
        chunk = (match.group(), match.start(), match.end(), True)  # (chunk_of_words, start, end, is_tagged)
        tagged_chunks.append(chunk)

    if len(tagged_chunks) == 0:
        tagged_chunks = [(sentence, 0, len(sentence), False)]  # TODO semantically wrong

    chunks = []
    for idx in range(0, len(tagged_chunks)):
        if idx == 0:
            if tagged_chunks[idx][1] > 0:  # first character is not tagged
                chunks.append((sentence[0:tagged_chunks[idx][1]], 0, tagged_chunks[idx][1], False))
                chunks.append(tagged_chunks[idx])
            else:
                chunks.append(tagged_chunks[idx])
        else:
            if tagged_chunks[idx][1] == tagged_chunks[idx - 1][2]:
                chunks.append(tagged_chunks[idx])
            elif tagged_chunks[idx][1] < tagged_chunks[idx - 1][2]:
                print("ERROR: found pattern has overlap!", tagged_chunks[idx][1], ' with ', tagged_chunks[idx - 1][2])
            else:
                chunks.append(
                    (sentence[tagged_chunks[idx - 1][2]:tagged_chunks[idx][1]], tagged_chunks[idx - 1][2],
                     tagged_chunks[idx][1],
                     False))
                chunks.append(tagged_chunks[idx])

        sent_len = len(sentence)
        if idx == len(tagged_chunks) - 1:
            if tagged_chunks[idx][2] > sent_len:
                print("ERROR: found pattern position larger than sentence length!")
            elif tagged_chunks[idx][2] < sent_len:
                chunks.append([sentence[tagged_chunks[idx][2]:sent_len], tagged_chunks[idx][2], sent_len, False])
            else:
                continue
    return turnFullListToOutputPair(chunks, segmented, tagScheme, onlyNP)



def ann_to_bio(save_path, file):
    fileLines = open(file, 'r', encoding="utf-8").readlines()
    lineNum = len(fileLines)

    file_name = file.split("\\")[-1][:-4]  # eg：data_10
    new_filename = save_path + file_name + ".bio"

    seqFile = open(new_filename, 'w', encoding="utf-8")
    for line in fileLines:
        if len(line) <= 2:
            seqFile.write('\n')
            continue
        else:
            # if not False:
            #     line = removeRecommendContent(line, self.recommendRe)
            #     pattern = self.entity_regex
            # else:
            #     pattern = "\[[\@\$)].*?\#.*?\*\](?!\#)"
            # print(dlg.segmented(), dlg.tag_scheme(), dlg.only_NP(), pattern) # False BIO False \[[\@\$)].*?\#.*?\*\](?!\#)
            pattern = '\\[[\\@\\$)].*?\\#.*?\\*\\](?!\\#)'
            wordTagPairs = getWordTagPairs(line, False, "BIO", False, pattern)
            for wordTag in wordTagPairs:
                seqFile.write(wordTag)
            # use null line to separate sentences
            seqFile.write('\n')
    seqFile.close()
    print("Exported file into sequence style in file: ", new_filename)
    print("Line number:", lineNum)

    return new_filename   # 返回文件路径


def ann_to_bmes(save_path,file):
    fileLines = open(file, 'r', encoding="utf-8").readlines()
    lineNum = len(fileLines)

    file_name = file.split("\\")[-1][:-4]  # eg：data_10
    new_filename = save_path + file_name + ".bmes"
    seqFile = open(new_filename, 'w', encoding="utf-8")
    for line in fileLines:
        if len(line) <= 2:
            seqFile.write('\n')
            continue
        else:
            # if not False:
            #     line = removeRecommendContent(line, self.recommendRe)
            #     pattern = self.entity_regex
            # else:
            #     pattern = "\[[\@\$)].*?\#.*?\*\](?!\#)"
            # print(dlg.segmented(), dlg.tag_scheme(), dlg.only_NP(), pattern) # False BIO False \[[\@\$)].*?\#.*?\*\](?!\#)
            pattern = '\\[[\\@\\$)].*?\\#.*?\\*\\](?!\\#)'
            wordTagPairs = getWordTagPairs(line, False, "BMES", False, pattern)
            for wordTag in wordTagPairs:
                seqFile.write(wordTag)
            # use null line to separate sentences
            seqFile.write('\n')
    seqFile.close()
    print("Exported file into sequence style in file: ", new_filename)
    print("Line number:", lineNum)

    return new_filename  # 返回文件路径


# 测试代码
if __name__ == "__main__":
    ann_to_bmes("ann/众包/pre_mark1-500.ann")
