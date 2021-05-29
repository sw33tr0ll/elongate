import { AnalysisDto } from "../models/AnalysisDto";

export class AnalysisResponse {
  tweet: string;
  body: any;

  static FromDto(analysisDto: AnalysisDto | {}): AnalysisResponse {

    var analysis = new AnalysisResponse();

    if (analysisDto['data']['error']) {
      analysis.body = analysisDto['data']['error'];
    }
    else {
      analysis.body = analysisDto['data']['tweet'];
    }

    return analysis;
  }
}
