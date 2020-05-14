var GaussianNB = function(priors, sigmas, thetas) {

    this.priors = priors;
    this.sigmas = sigmas;
    this.thetas = thetas;

    this.predict = function(features) {
        var likelihoods = new Array(this.sigmas.length);
    
        for (var i = 0, il = this.sigmas.length; i < il; i++) {
            var sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.log(2. * Math.PI * this.sigmas[i][j]);
            }
            var nij = -0.5 * sum;
            sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.pow(features[j] - this.thetas[i][j], 2.) / this.sigmas[i][j];
            }
            nij -= 0.5 * sum;
            likelihoods[i] = Math.log(this.priors[i]) + nij;
        }
    
        var classIdx = 0;
        for (var i = 0, l = likelihoods.length; i < l; i++) {
            classIdx = likelihoods[i] > likelihoods[classIdx] ? i : classIdx;
        }
        return classIdx;
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 8) {

        // Features:
        var features = process.argv.slice(2);

        // Parameters:
        var priors = [0.45257184158044783, 0.5474281584195522];
        var sigmas = [[1.6822780338779746, 0.43675097210765945, 1.0000000000191261e-09, 4.523060926326598e-05, 2.205335768248672, 0.0877686092282645, 1.7495989641551721, 0.7314799617871321], [0.3614647800539146, 1.3996616276661118, 1.8263370081202697, 1.8266819799499188, 0.00024189379517133887, 1.542484821985828, 0.37533133365486776, 1.1458864464324587]];
        var thetas = [[-0.22207649266435125, -0.2090361786074277, -0.01600205089471235, -0.0016962078219578559, 0.04659262046679472, -0.37438785192175744, 0.05729431342547847, -0.22448701062556647], [0.18359590333669124, 0.1728151664365392, 0.013229274985388163, 0.0014022952343129152, -0.03851922434820412, 0.3095153163102484, -0.047366567722884355, 0.18558873570266374]];

        // Estimator:
        var clf = new GaussianNB(priors, sigmas, thetas);
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}